#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pwd
import re
import subprocess
import tarfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "zorin-stock-wallpapers-17.3.json"
CURRENT_NAME = "current"


def fail(message: str) -> "NoReturn":
    raise SystemExit(f"ERROR: {message}")


def run(
    args: list[str],
    *,
    check: bool = True,
    cwd: Path | None = None,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=check,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
    )


class Workflow:
    def __init__(self) -> None:
        self.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.target = self.data["target"]
        self.packages = [(item["name"], item["version"]) for item in self.data["packages"]]
        self.paths = [
            (item["path"], item["owner"])
            for item in self.data["catalogs"] + self.data["wallpaper_files"]
        ]
        self.recovery_root = Path(self.data["recovery_root"])
        self.current_file = self.recovery_root / CURRENT_NAME

    def desktop_user(self) -> str:
        sudo_user = os.environ.get("SUDO_USER")
        if sudo_user and sudo_user != "root":
            return sudo_user
        return pwd.getpwuid(os.getuid()).pw_name

    def desktop_home(self) -> Path:
        user = self.desktop_user()
        if user == "root":
            fail("run from the desktop user account; use sudo only for privileged subcommands")
        return Path(pwd.getpwnam(user).pw_dir)

    @staticmethod
    def expand_user_path(home: Path, value: str) -> Path:
        if value.startswith("~/"):
            return home / value[2:]
        return Path(value)

    def verify_os(self) -> None:
        values: dict[str, str] = {}
        for raw in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
            if "=" not in raw or raw.startswith("#"):
                continue
            key, value = raw.split("=", 1)
            values[key] = value.strip().strip('"')
        if values.get("ID") != self.target["id"]:
            fail(f"expected OS ID {self.target['id']}; found {values.get('ID', 'unknown')}")
        if self.target["version"] not in values.get("VERSION", ""):
            fail(
                f"expected Zorin version {self.target['version']}; "
                f"found {values.get('VERSION', 'unknown')}"
            )

    @staticmethod
    def dpkg_field(package: str, field: str) -> str:
        result = run(["dpkg-query", "-W", f"-f=${{{field}}}", package], check=False)
        return result.stdout.strip() if result.returncode == 0 else ""

    def verify_packages_exact(self) -> None:
        for name, expected in self.packages:
            actual = self.dpkg_field(name, "Version")
            if actual != expected:
                fail(f"expected {name} version {expected}; found {actual or 'not installed'}")

    def verify_stock_paths_present(self) -> None:
        for path_text, owner in self.paths:
            path = Path(path_text)
            if not path.is_file():
                fail(f"expected audited stock path is missing: {path}")
            result = run(["dpkg-query", "-S", str(path)], check=False)
            expected = f"{owner}: {path}"
            if result.returncode != 0 or expected not in result.stdout.splitlines():
                fail(f"package ownership changed for {path}; expected {owner}")

    def verify_stock_paths_absent(self) -> None:
        for path_text, owner in self.paths:
            if Path(path_text).exists():
                fail(f"stock wallpaper path is still present: {path_text} ({owner})")

    def replacement_paths(self) -> tuple[Path, Path, int]:
        home = self.desktop_home()
        repl = self.data["replacement"]
        return (
            self.expand_user_path(home, repl["user_background_dir"]),
            self.expand_user_path(home, repl["user_catalog"]),
            int(repl["expected_wallpaper_count"]),
        )

    def verify_replacement_ready(self, *, announce: bool = True) -> None:
        bg_dir, catalog, expected = self.replacement_paths()
        if not bg_dir.is_dir():
            fail(f"GoreeCloud wallpaper directory is missing: {bg_dir}")
        if not catalog.is_file():
            fail(f"GoreeCloud user background catalog is missing: {catalog}")
        root = ET.parse(catalog).getroot()
        nodes = root.findall("wallpaper")
        if len(nodes) != expected:
            fail(f"expected {expected} GoreeCloud catalog entries; found {len(nodes)}")
        resolved_root = bg_dir.resolve()
        for node in nodes:
            filename = node.findtext("filename")
            if not filename:
                fail("GoreeCloud catalog entry is missing filename")
            path = Path(filename).resolve()
            if path.parent != resolved_root:
                fail(f"GoreeCloud catalog entry escapes replacement directory: {path}")
            if not path.is_file():
                fail(f"GoreeCloud catalog wallpaper is missing: {path}")
        if announce:
            print(f"Replacement catalog ready for {self.desktop_user()}: {len(nodes)} wallpapers")

    def package_names(self) -> list[str]:
        return [name for name, _version in self.packages]

    def package_specs(self) -> list[str]:
        return [f"{name}={version}" for name, version in self.packages]

    def simulate_purge(self) -> str:
        result = run(["apt-get", "--simulate", "purge", *self.package_names()], check=False)
        if result.returncode != 0:
            fail(f"apt purge simulation failed:\n{result.stdout}")
        removed = sorted(
            {
                match.group(2)
                for line in result.stdout.splitlines()
                if (match := re.match(r"^(Remv|Purg)\s+(\S+)", line))
            }
        )
        expected = sorted(self.package_names())
        if removed != expected:
            fail(
                "apt simulation removal set differs from the four audited wallpaper packages.\n"
                f"Expected: {expected}\nObserved: {removed}\n\n{result.stdout}"
            )
        return result.stdout

    def current_recovery(self) -> Path:
        if not self.current_file.is_file():
            fail("no active GoreeCloud wallpaper recovery transaction exists")
        recovery = Path(self.current_file.read_text(encoding="utf-8").strip())
        try:
            recovery.resolve().relative_to(self.recovery_root.resolve())
        except ValueError:
            fail(f"recovery pointer escaped the expected root: {recovery}")
        if not recovery.is_dir():
            fail(f"recovery directory is missing: {recovery}")
        return recovery

    @staticmethod
    def hash_file(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def write_checksums(self, recovery: Path) -> None:
        lines = [f"{self.hash_file(Path(path))}\t{path}\n" for path, _owner in self.paths]
        (recovery / "stock-files.sha256.tsv").write_text("".join(lines), encoding="utf-8")

    def verify_checksums(self, recovery: Path) -> None:
        checksum_file = recovery / "stock-files.sha256.tsv"
        for raw in checksum_file.read_text(encoding="utf-8").splitlines():
            digest, path_text = raw.split("\t", 1)
            path = Path(path_text)
            if not path.is_file():
                fail(f"restored stock file is missing: {path}")
            if self.hash_file(path) != digest:
                fail(f"restored stock file checksum differs: {path}")

    def create_recovery(self) -> Path:
        self.recovery_root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.recovery_root, 0o700)
        if self.current_file.exists():
            fail("an unfinished wallpaper recovery transaction already exists; restore or finalize it first")

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        recovery = self.recovery_root / stamp
        packages_dir = recovery / "packages"
        packages_dir.mkdir(parents=True, mode=0o700)

        relative_paths = [path.lstrip("/") for path, _owner in self.paths]
        run(
            ["tar", "-C", "/", "-cpf", str(recovery / "stock-files.tar"), *relative_paths],
            capture=False,
        )
        self.write_checksums(recovery)

        package_lines = []
        for name, version in self.packages:
            status = self.dpkg_field(name, "db:Status-Abbrev")
            package_lines.append(f"{name}\t{version}\t{status}\n")
        (recovery / "packages.tsv").write_text("".join(package_lines), encoding="utf-8")

        simulation = self.simulate_purge()
        (recovery / "apt-purge-simulation.txt").write_text(simulation, encoding="utf-8")

        result = run(["apt-get", "download", *self.package_specs()], cwd=packages_dir, check=False)
        if result.returncode != 0:
            fail(
                "could not download the exact wallpaper .deb recovery set; "
                f"refusing removal.\n{result.stdout}"
            )
        debs = sorted(packages_dir.glob("*.deb"))
        if len(debs) != len(self.packages):
            fail(f"expected {len(self.packages)} recovery .deb files; found {len(debs)}")

        (recovery / "state").write_text("prepared\n", encoding="utf-8")
        self.current_file.write_text(f"{recovery}\n", encoding="utf-8")
        return recovery

    def require_root(self) -> None:
        if os.geteuid() != 0:
            fail("this subcommand requires sudo/root")
        sudo_user = os.environ.get("SUDO_USER")
        if not sudo_user or sudo_user == "root":
            fail("invoke this command with sudo from the desktop user account")

    def plan(self) -> None:
        self.verify_os()
        self.verify_packages_exact()
        self.verify_stock_paths_present()
        self.verify_replacement_ready()
        simulation = self.simulate_purge()
        print("\nAudited stock set:")
        print(f"  packages: {len(self.packages)}")
        print(f"  package-owned wallpaper/catalog paths: {len(self.paths)}")
        print("\napt purge simulation (read-only):")
        print(simulation.rstrip())
        print(
            "\nPLAN PASSED: apt proposes removal of exactly the four audited "
            "wallpaper packages and no others.\nNo files or packages were changed."
        )

    def apply(self) -> None:
        self.require_root()
        self.verify_os()
        self.verify_packages_exact()
        self.verify_stock_paths_present()
        self.verify_replacement_ready()

        recovery = self.create_recovery()
        print(f"Recovery material prepared at:\n  {recovery}")

        result = run(["apt-get", "purge", "--yes", *self.package_names()], check=False, capture=False)
        if result.returncode != 0:
            fail(
                "apt purge failed. Recovery remains prepared; "
                "run sudo ./scripts/system_wallpapers.sh restore before further changes."
            )

        for name, _version in self.packages:
            if self.dpkg_field(name, "db:Status-Abbrev").startswith("ii"):
                fail(f"package is still installed after purge: {name}")
        self.verify_stock_paths_absent()
        self.verify_replacement_ready()
        (recovery / "state").write_text("removed\n", encoding="utf-8")
        print(
            "\nStock Zorin wallpaper packages were removed without collateral package removal.\n"
            "Recovery remains available until visual acceptance and finalize."
        )

    def restore(self) -> None:
        self.require_root()
        self.verify_os()
        recovery = self.current_recovery()
        state = (recovery / "state").read_text(encoding="utf-8").strip()
        if state not in {"prepared", "removed"}:
            fail(f"recovery state is not restorable: {state}")

        debs = sorted((recovery / "packages").glob("*.deb"))
        if len(debs) != len(self.packages):
            fail("recovery .deb set is incomplete")
        result = run(["apt-get", "install", "--yes", *map(str, debs)], check=False, capture=False)
        if result.returncode != 0:
            fail("reinstalling the archived stock wallpaper packages failed")

        expected_members = {path.lstrip("/") for path, _owner in self.paths}
        with tarfile.open(recovery / "stock-files.tar", "r") as archive:
            members = archive.getmembers()
            observed = {member.name for member in members if member.isfile()}
            if observed != expected_members:
                fail("recovery archive member set differs from the audited stock paths")
            for member in members:
                member_path = Path(member.name)
                if member_path.is_absolute() or ".." in member_path.parts:
                    fail(f"unsafe recovery archive member: {member.name}")
            archive.extractall(path="/")
        self.verify_checksums(recovery)
        self.verify_packages_exact()
        self.verify_stock_paths_present()

        (recovery / "state").write_text("restored\n", encoding="utf-8")
        self.current_file.unlink(missing_ok=True)
        print(f"Restored the audited Zorin stock wallpaper package/fileset from:\n  {recovery}")

    def finalize(self) -> None:
        self.require_root()
        self.verify_os()
        recovery = self.current_recovery()
        state = (recovery / "state").read_text(encoding="utf-8").strip()
        if state != "removed":
            fail(f"finalize is allowed only after a successful removal; current state: {state}")
        self.verify_stock_paths_absent()
        self.verify_replacement_ready()
        for name, _version in self.packages:
            if self.dpkg_field(name, "db:Status-Abbrev").startswith("ii"):
                fail(f"cannot finalize while stock package remains installed: {name}")

        resolved = recovery.resolve()
        if resolved == self.recovery_root.resolve():
            fail("refusing to delete the recovery root itself")
        resolved.relative_to(self.recovery_root.resolve())

        for root_text, dirs, files in os.walk(resolved, topdown=False):
            root = Path(root_text)
            for filename in files:
                (root / filename).unlink()
            for dirname in dirs:
                (root / dirname).rmdir()
        resolved.rmdir()
        self.current_file.unlink(missing_ok=True)
        print(
            "Recovery copy deleted. Stock Zorin wallpaper removal is now "
            "irreversible through this helper."
        )

    def status(self) -> None:
        self.verify_os()
        print(f"Target: {self.target['id']} {self.target['version']}\n")
        print("Audited stock packages:")
        for name, expected in self.packages:
            version = self.dpkg_field(name, "Version")
            status = self.dpkg_field(name, "db:Status-Abbrev")
            current = f"{version} {status}".strip() if version else "not installed"
            print(f"  {name:<32} expected {expected:<8} current {current}")

        present = sum(1 for path, _owner in self.paths if Path(path).exists())
        print(f"\nAudited stock paths still present: {present} / {len(self.paths)}")
        print("\nGoreeCloud replacement:")
        self.verify_replacement_ready()

        print("\nRecovery transaction:")
        if self.current_file.is_file():
            recovery = Path(self.current_file.read_text(encoding="utf-8").strip())
            print(f"  {recovery}")
            state_file = recovery / "state"
            if state_file.is_file():
                print(f"  state: {state_file.read_text(encoding='utf-8').strip()}")
        else:
            print("  none")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evidence-bound Zorin OS 17.3 stock wallpaper removal and recovery."
    )
    parser.add_argument("action", choices=("plan", "apply", "status", "restore", "finalize"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workflow = Workflow()
    getattr(workflow, args.action)()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

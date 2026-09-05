#!/usr/bin/env python3
from __future__ import annotations

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
from typing import NoReturn

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "zorin-stock-wallpapers-17.3.json"
CURRENT_NAME = "current"


def fail(message: str) -> NoReturn:
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
        if self.data.get("schema_version") != 2:
            fail("unsupported stock wallpaper manifest schema")
        self.target = self.data["target"]
        self.packages = [(item["name"], item["version"]) for item in self.data["packages"]]
        strategy = self.data["strategy"]
        if strategy.get("mode") != "dpkg-divert" or strategy.get("package_purge") != "prohibited":
            fail("stock wallpaper strategy must be package-safe dpkg-divert")
        self.protected_packages = [
            (item["name"], item["version"])
            for item in strategy.get("protected_packages", [])
        ]
        self.paths = [
            (item["path"], item["owner"])
            for item in self.data["catalogs"] + self.data["wallpaper_files"]
        ]
        self.recovery_root = Path(self.data["recovery_root"])
        self.diversion_root = Path(strategy["diversion_root"])
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

    def verify_package_list_exact(self, packages: list[tuple[str, str]], label: str) -> None:
        for name, expected in packages:
            actual = self.dpkg_field(name, "Version")
            status = self.dpkg_field(name, "db:Status-Abbrev")
            if actual != expected or not status.startswith("ii"):
                current = f"{actual or 'not installed'} {status}".strip()
                fail(f"expected {label} package {name} {expected} installed; found {current}")

    def verify_packages_exact(self) -> None:
        self.verify_package_list_exact(self.packages, "wallpaper")
        self.verify_package_list_exact(self.protected_packages, "protected Zorin")

    def verify_stock_paths_present(self) -> None:
        for path_text, owner in self.paths:
            path = Path(path_text)
            if not path.is_file():
                fail(f"expected audited stock path is missing: {path}")
            result = run(["dpkg-query", "-S", str(path)], check=False)
            expected = f"{owner}: {path}"
            if result.returncode != 0 or expected not in result.stdout.splitlines():
                fail(f"package ownership changed for {path}; expected {owner}")

    def diversion_target(self, path_text: str) -> Path:
        original = Path(path_text)
        if not original.is_absolute():
            fail(f"audited stock path is not absolute: {path_text}")
        target = self.diversion_root / path_text.lstrip("/")
        try:
            target.resolve(strict=False).relative_to(self.diversion_root.resolve(strict=False))
        except ValueError:
            fail(f"diversion target escaped diversion root: {target}")
        return target

    def diversion_registered(self, path_text: str, target: Path) -> bool:
        result = run(["dpkg-divert", "--list", path_text], check=False)
        if result.returncode != 0:
            return False
        expected = f"local diversion of {path_text} to {target}"
        return expected in result.stdout.splitlines()

    def active_diversion_count(self) -> int:
        count = 0
        for path_text, _owner in self.paths:
            target = self.diversion_target(path_text)
            if self.diversion_registered(path_text, target):
                count += 1
        return count

    def verify_stock_paths_diverted(self) -> None:
        for path_text, _owner in self.paths:
            original = Path(path_text)
            target = self.diversion_target(path_text)
            if original.exists():
                fail(f"stock wallpaper path remains in GNOME discovery location: {original}")
            if not target.is_file():
                fail(f"diverted stock file is missing: {target}")
            if not self.diversion_registered(path_text, target):
                fail(f"dpkg diversion is not registered for {path_text}")

    def verify_no_partial_diversions(self) -> None:
        active = self.active_diversion_count()
        if active not in {0, len(self.paths)}:
            fail(
                f"partial stock wallpaper diversion state detected: {active}/{len(self.paths)}. "
                "Run sudo ./scripts/system_wallpapers.sh restore before continuing."
            )

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

    def simulate_purge_diagnostic(self) -> tuple[str, list[str], list[str]]:
        names = [name for name, _version in self.packages]
        result = run(["apt-get", "--simulate", "purge", *names], check=False)
        removed = sorted(
            {
                match.group(2)
                for line in result.stdout.splitlines()
                if (match := re.match(r"^(Remv|Purg)\s+(\S+)", line))
            }
        )
        installed = sorted(
            {
                match.group(1)
                for line in result.stdout.splitlines()
                if (match := re.match(r"^Inst\s+(\S+)", line))
            }
        )
        return result.stdout, removed, installed

    def current_recovery(self, *, required: bool = True) -> Path | None:
        try:
            current_exists = self.current_file.is_file()
        except PermissionError:
            if required:
                fail("recovery transaction metadata is root-owned; rerun this subcommand with sudo")
            return None
        if not current_exists:
            if required:
                fail("no active GoreeCloud wallpaper recovery transaction exists")
            return None
        try:
            recovery = Path(self.current_file.read_text(encoding="utf-8").strip())
        except PermissionError:
            if required:
                fail("recovery transaction metadata is root-owned; rerun this subcommand with sudo")
            return None
        try:
            recovery.resolve().relative_to(self.recovery_root.resolve())
        except ValueError:
            fail(f"recovery pointer escaped the expected root: {recovery}")
        try:
            recovery_exists = recovery.is_dir()
        except PermissionError:
            if required:
                fail("recovery transaction directory is root-owned; rerun this subcommand with sudo")
            return None
        if not recovery_exists:
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
        if not checksum_file.is_file():
            return
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
        if self.active_diversion_count() != 0:
            fail("stock wallpaper diversions already exist without an active recovery transaction")

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        recovery = self.recovery_root / stamp
        recovery.mkdir(parents=True, mode=0o700)

        relative_paths = [path.lstrip("/") for path, _owner in self.paths]
        run(
            ["tar", "-C", "/", "-cpf", str(recovery / "stock-files.tar"), *relative_paths],
            capture=False,
        )
        self.write_checksums(recovery)

        package_lines = []
        for name, version in self.packages + self.protected_packages:
            status = self.dpkg_field(name, "db:Status-Abbrev")
            package_lines.append(f"{name}\t{version}\t{status}\n")
        (recovery / "packages.tsv").write_text("".join(package_lines), encoding="utf-8")

        simulation, removed, installed = self.simulate_purge_diagnostic()
        (recovery / "apt-purge-simulation.txt").write_text(simulation, encoding="utf-8")
        (recovery / "apt-purge-observed.json").write_text(
            json.dumps({"removed": removed, "installed": installed}, indent=2) + "\n",
            encoding="utf-8",
        )

        (recovery / "state").write_text("prepared\n", encoding="utf-8")
        self.current_file.write_text(f"{recovery}\n", encoding="utf-8")
        return recovery

    def require_root(self) -> None:
        if os.geteuid() != 0:
            fail("this subcommand requires sudo/root")
        sudo_user = os.environ.get("SUDO_USER")
        if not sudo_user or sudo_user == "root":
            fail("invoke this command with sudo from the desktop user account")

    def add_diversion(self, path_text: str) -> None:
        target = self.diversion_target(path_text)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            fail(f"diversion destination already exists: {target}")
        result = run(
            [
                "dpkg-divert",
                "--local",
                "--add",
                "--rename",
                "--divert",
                str(target),
                path_text,
            ],
            check=False,
            capture=False,
        )
        if result.returncode != 0:
            fail(f"dpkg-divert failed for {path_text}")

    def remove_diversion(self, path_text: str) -> None:
        target = self.diversion_target(path_text)
        original = Path(path_text)
        registered = self.diversion_registered(path_text, target)
        if not registered:
            if original.is_file() and not target.exists():
                return
            fail(f"cannot restore unregistered or inconsistent diversion for {path_text}")
        result = run(
            [
                "dpkg-divert",
                "--local",
                "--remove",
                "--rename",
                "--divert",
                str(target),
                path_text,
            ],
            check=False,
            capture=False,
        )
        if result.returncode != 0:
            fail(f"removing dpkg diversion failed for {path_text}")

    def prune_empty_diversion_dirs(self) -> None:
        if not self.diversion_root.exists():
            return
        for root_text, dirs, files in os.walk(self.diversion_root, topdown=False):
            root = Path(root_text)
            if files:
                continue
            for dirname in dirs:
                child = root / dirname
                try:
                    child.rmdir()
                except OSError:
                    pass
        try:
            self.diversion_root.rmdir()
        except OSError:
            pass

    def delete_recovery_tree(self, recovery: Path) -> None:
        resolved = recovery.resolve()
        root_resolved = self.recovery_root.resolve()
        if resolved == root_resolved:
            fail("refusing to delete the recovery root itself")
        resolved.relative_to(root_resolved)
        for root_text, dirs, files in os.walk(resolved, topdown=False):
            root = Path(root_text)
            for filename in files:
                (root / filename).unlink()
            for dirname in dirs:
                (root / dirname).rmdir()
        resolved.rmdir()

    def plan(self) -> None:
        self.verify_os()
        self.verify_packages_exact()
        self.verify_no_partial_diversions()
        active = self.active_diversion_count()
        if active == len(self.paths):
            fail("stock wallpaper replacement is already active")
        self.verify_stock_paths_present()
        self.verify_replacement_ready()

        simulation, removed, installed = self.simulate_purge_diagnostic()
        expected_wallpaper = {name for name, _version in self.packages}
        collateral = sorted(set(removed) - expected_wallpaper)

        print("\nAudited stock set:")
        print(f"  packages kept installed: {len(self.packages)}")
        print(f"  protected Zorin packages: {len(self.protected_packages)}")
        print(f"  package-owned wallpaper/catalog paths to divert: {len(self.paths)}")
        print(f"  diversion root: {self.diversion_root}")

        print("\nDirect apt purge diagnostic (read-only; purge will NOT be used):")
        print(simulation.rstrip())
        if collateral or installed:
            print("\nPackage purge rejected by design:")
            if collateral:
                print(f"  additional removals: {', '.join(collateral)}")
            if installed:
                print(f"  additional installs: {', '.join(installed)}")

        print(
            "\nPLAN PASSED: replacement will keep every Zorin package installed and "
            "use local dpkg diversions to move only the audited wallpaper images and "
            "GNOME background catalogs out of discovery paths. No files or packages were changed."
        )

    def apply(self) -> None:
        self.require_root()
        self.verify_os()
        self.verify_packages_exact()
        self.verify_no_partial_diversions()
        if self.active_diversion_count() == len(self.paths):
            fail("stock wallpaper replacement is already active")
        self.verify_stock_paths_present()
        self.verify_replacement_ready()

        recovery = self.create_recovery()
        print(f"Recovery material prepared at:\n  {recovery}")

        try:
            for path_text, _owner in self.paths:
                self.add_diversion(path_text)
        except BaseException:
            print(
                "A diversion failed before completion. Recovery remains prepared.\n"
                "Run: sudo ./scripts/system_wallpapers.sh restore",
                flush=True,
            )
            raise

        self.verify_stock_paths_diverted()
        self.verify_packages_exact()
        self.verify_replacement_ready()
        (recovery / "state").write_text("diverted\n", encoding="utf-8")
        print(
            "\nStock Zorin wallpaper files and catalogs are now outside GNOME discovery paths.\n"
            "All Zorin packages, including zorin-os-artwork and zorin-os-desktop, remain installed.\n"
            "Recovery remains available through the restore command."
        )

    def restore(self) -> None:
        self.require_root()
        self.verify_os()
        self.verify_packages_exact()
        recovery = self.current_recovery(required=False)
        active = self.active_diversion_count()
        if active == 0:
            if recovery is not None:
                fail("recovery transaction exists but no stock wallpaper diversions are active")
            fail("no active GoreeCloud stock wallpaper diversions exist")
        if active != len(self.paths):
            print(f"Restoring partial diversion state: {active}/{len(self.paths)}")

        for path_text, _owner in reversed(self.paths):
            target = self.diversion_target(path_text)
            if self.diversion_registered(path_text, target):
                self.remove_diversion(path_text)

        self.prune_empty_diversion_dirs()
        self.verify_stock_paths_present()
        self.verify_packages_exact()
        if recovery is not None:
            self.verify_checksums(recovery)
            (recovery / "state").write_text("restored\n", encoding="utf-8")
            self.current_file.unlink(missing_ok=True)
            print(f"Restored the audited Zorin stock wallpaper files from diversions.\nRecovery record:\n  {recovery}")
        else:
            print("Restored the audited Zorin stock wallpaper files from finalized diversions.")

    def finalize(self) -> None:
        self.require_root()
        self.verify_os()
        self.verify_packages_exact()
        recovery = self.current_recovery()
        state = (recovery / "state").read_text(encoding="utf-8").strip()
        if state != "diverted":
            fail(f"finalize is allowed only after successful diversion; current state: {state}")
        self.verify_stock_paths_diverted()
        self.verify_replacement_ready()

        self.delete_recovery_tree(recovery)
        self.current_file.unlink(missing_ok=True)
        print(
            "Temporary recovery archive deleted. Package-safe dpkg diversions remain active, "
            "so stock wallpapers stay out of GNOME discovery paths across package reinstalls/updates. "
            "The restore command can still reverse the active diversions while the target package "
            "versions remain compatible."
        )

    def status(self) -> None:
        self.verify_os()
        print(f"Target: {self.target['id']} {self.target['version']}\n")
        print("Audited wallpaper packages (kept installed):")
        for name, expected in self.packages:
            version = self.dpkg_field(name, "Version")
            status = self.dpkg_field(name, "db:Status-Abbrev")
            current = f"{version} {status}".strip() if version else "not installed"
            print(f"  {name:<32} expected {expected:<8} current {current}")

        print("\nProtected Zorin packages:")
        for name, expected in self.protected_packages:
            version = self.dpkg_field(name, "Version")
            status = self.dpkg_field(name, "db:Status-Abbrev")
            current = f"{version} {status}".strip() if version else "not installed"
            print(f"  {name:<32} expected {expected:<8} current {current}")

        present = sum(1 for path, _owner in self.paths if Path(path).exists())
        active = self.active_diversion_count()
        print(f"\nAudited stock paths in original discovery locations: {present} / {len(self.paths)}")
        print(f"Active package-safe diversions: {active} / {len(self.paths)}")
        print("\nGoreeCloud replacement:")
        self.verify_replacement_ready()

        print("\nRecovery transaction:")
        if os.geteuid() != 0:
            if active:
                print("  package-safe diversions are active")
                print("  recovery/finalization metadata is root-owned")
                print("  transaction details: sudo ./scripts/system_wallpapers.sh status")
            else:
                print("  none")
            return

        recovery = self.current_recovery(required=False)
        if recovery is not None:
            print(f"  {recovery}")
            state_file = recovery / "state"
            if state_file.is_file():
                print(f"  state: {state_file.read_text(encoding='utf-8').strip()}")
        elif active:
            print("  finalized; diversions remain active")
        else:
            print("  none")


def parse_args() -> object:
    import argparse

    parser = argparse.ArgumentParser(
        description="Evidence-bound Zorin OS 17.3 stock wallpaper replacement and recovery."
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

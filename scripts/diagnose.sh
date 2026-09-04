#!/usr/bin/env bash
set -u

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

section() {
  printf '\n== %s ==\n' "$1"
}

print_command() {
  local label="$1"
  local output
  shift
  printf '%-28s' "$label"
  if output="$("$@" 2>/dev/null)"; then
    printf '%s\n' "$output"
  else
    printf '%s\n' "unavailable"
  fi
}

print_gsetting() {
  local label="$1"
  local schema="$2"
  local key="$3"
  local output
  printf '%-28s' "$label"
  if output="$(gsettings get "$schema" "$key" 2>/dev/null)"; then
    printf '%s\n' "$output"
  else
    printf '%s\n' "unavailable"
  fi
}

printf '%s\n' "GoreeCloud Zorin OS theme diagnostic (read-only)"
printf '%s\n' "This script changes no settings and writes no system files."

section "Repository"
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  print_command "commit" git -C "$ROOT" rev-parse HEAD
  print_command "branch" git -C "$ROOT" branch --show-current
else
  printf '%s\n' "Repository metadata unavailable"
fi

section "Operating system and session"
if [[ -r /etc/os-release ]]; then
  grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release || true
fi
printf '%-28s%s\n' "XDG_SESSION_TYPE" "${XDG_SESSION_TYPE:-unset}"
printf '%-28s%s\n' "XDG_CURRENT_DESKTOP" "${XDG_CURRENT_DESKTOP:-unset}"
printf '%-28s%s\n' "DESKTOP_SESSION" "${DESKTOP_SESSION:-unset}"
print_command "GNOME Shell" gnome-shell --version
print_command "Files / Nautilus" nautilus --version

section "Relevant package versions"
for package in \
  zorin-desktop-themes \
  zorin-appearance \
  nautilus \
  libadwaita-1-0 \
  gnome-shell; do
  printf '%-28s' "$package"
  if version="$(dpkg-query -W -f='${Version}' "$package" 2>/dev/null)"; then
    printf '%s\n' "$version"
  else
    printf '%s\n' "not found"
  fi
done

section "Current theme settings"
print_gsetting "GTK theme" org.gnome.desktop.interface gtk-theme
print_gsetting "color scheme" org.gnome.desktop.interface color-scheme
print_gsetting "Shell user theme" org.gnome.shell.extensions.user-theme name

section "Installed GoreeCloud theme files"
shopt -s nullglob
installed=("${HOME}/.local/share/themes/GoreeCloud-Zorin-"*)
if (( ${#installed[@]} == 0 )); then
  printf '%s\n' "No GoreeCloud-Zorin-* theme directories found under ~/.local/share/themes"
else
  find "${installed[@]}" -maxdepth 2 -type f -printf '%p\n' 2>/dev/null | sed "s|${HOME}|~|" | sort
fi
shopt -u nullglob

section "Installed Zorin base theme evidence"
base_files=()
for variant in ZorinBlue-Light ZorinBlue-Dark; do
  for relative in gtk-4.0/gtk.css gtk-4.0/gtk-dark.css gnome-shell/gnome-shell.css; do
    path="/usr/share/themes/${variant}/${relative}"
    if [[ -f "$path" ]]; then
      base_files+=("$path")
    fi
  done
done

if (( ${#base_files[@]} == 0 )); then
  printf '%s\n' "Expected ZorinBlue Light/Dark base theme files were not found in /usr/share/themes"
else
  for path in "${base_files[@]}"; do
    printf '%s\n' "$path"
    printf '  bytes:  '
    wc -c < "$path"
    printf '  sha256: '
    sha256sum "$path" | awk '{print $1}'
  done
fi

section "Why this output matters"
printf '%s\n' "The repository commit and installed package/theme evidence let development stay pinned to the actual Zorin OS 17.3 implementation instead of assuming current upstream theme internals."
printf '%s\n' "If Shell colors appear stale after a reinstall, log out and back in before treating Shell selector behavior as a source failure."

#!/usr/bin/env bash
set -u

section() {
  printf '\n== %s ==\n' "$1"
}

bounded_matches() {
  local label="$1"
  shift
  printf '%s\n' "$label"
  if ! "$@" 2>/dev/null | grep -nEi \
    'row:selected|row\.activatable:selected|navigation|sidebar|search|switch:checked|theme_selected_bg_color|selected_bg_color|#bde6fb|#BDE6FB' \
    | head -n 160 | sed 's/^/  /'; then
    printf '%s\n' "  no matching state selectors/tokens found"
  fi
}

resource_list() {
  local file="$1"
  local section_name="${2:-}"
  if [[ -n "$section_name" ]]; then
    gresource list --section "$section_name" "$file" 2>/dev/null
  else
    gresource list "$file" 2>/dev/null
  fi
}

resource_extract() {
  local file="$1"
  local section_name="$2"
  local resource="$3"
  if [[ -n "$section_name" ]]; then
    gresource extract --section "$section_name" "$file" "$resource" 2>/dev/null
  else
    gresource extract "$file" "$resource" 2>/dev/null
  fi
}

inspect_resource_container() {
  local label="$1"
  local file="$2"
  local section_name="${3:-}"
  local resources=()
  local resource

  [[ -r "$file" ]] || return 0
  command -v gresource >/dev/null 2>&1 || return 0

  if [[ -n "$section_name" ]]; then
    printf '%s\n' "$label: $file [$section_name]"
  else
    printf '%s\n' "$label: $file"
  fi

  mapfile -t resources < <(resource_list "$file" "$section_name")
  if (( ${#resources[@]} == 0 )); then
    printf '%s\n' "  no readable resources"
    return 0
  fi

  for resource in "${resources[@]}"; do
    case "$resource" in
      *.css|*.scss)
        printf '  resource: %s\n' "$resource"
        resource_extract "$file" "$section_name" "$resource" \
          | grep -nEi \
            'row:selected|row\.activatable:selected|navigation|sidebar|search|switch:checked|theme_selected_bg_color|selected_bg_color|#bde6fb|#BDE6FB' \
          | head -n 160 \
          | sed 's/^/    /' || true
        ;;
    esac
  done
}

printf '%s\n' "GoreeCloud Settings GTK 3/libhandy CSS diagnostic (read-only)"
printf '%s\n' "This helper changes no settings, packages, themes, or system files."
printf '%s\n' "It inspects installed package files and embedded resources only."

SETTINGS_BIN="$(command -v gnome-control-center 2>/dev/null || true)"
HANDY_LIB="$(ldconfig -p 2>/dev/null | awk '/libhandy-1\.so\.0/{print $NF; exit}')"
ACTIVE_THEME="$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | tr -d "'" || true)"
ACTIVE_GTK3="${HOME}/.local/share/themes/${ACTIVE_THEME}/gtk-3.0/gtk.css"

section "Settings package and toolkit identity"
printf '%-28s%s\n' "Settings executable" "${SETTINGS_BIN:-unavailable}"
printf '%-28s%s\n' "Active GTK theme" "${ACTIVE_THEME:-unavailable}"
for package in gnome-control-center gnome-control-center-data libhandy-1-0; do
  printf '%-28s' "$package"
  if version="$(dpkg-query -W -f='${Version}' "$package" 2>/dev/null)"; then
    printf '%s\n' "$version"
  else
    printf '%s\n' "not found"
  fi
done

if [[ -n "$SETTINGS_BIN" && -r "$SETTINGS_BIN" ]]; then
  printf '%s\n' "Direct toolkit linkage:"
  ldd "$SETTINGS_BIN" 2>/dev/null \
    | grep -Ei 'libgtk|libgdk|libadwaita|libhandy' \
    | sed 's/^/  /' || true
fi

section "Active GoreeCloud GTK 3 selected-state rules"
if [[ -r "$ACTIVE_GTK3" ]]; then
  bounded_matches "Installed active-theme GTK 3 evidence: $ACTIVE_GTK3" cat "$ACTIVE_GTK3"
else
  printf '%s\n' "Active user-local GTK 3 stylesheet unavailable: $ACTIVE_GTK3"
fi

section "Packaged CSS and GResource candidates"
package_files=()
mapfile -t package_files < <(
  dpkg-query -L gnome-control-center gnome-control-center-data libhandy-1-0 2>/dev/null \
    | sort -u
)

candidate_count=0
for file in "${package_files[@]}"; do
  if [[ -f "$file" && ( "$file" == *.css || "$file" == *.scss || "$file" == *.gresource ) ]]; then
    printf '%s\n' "$file"
    candidate_count=$((candidate_count + 1))
  fi
done
if (( candidate_count == 0 )); then
  printf '%s\n' "No standalone CSS/GResource files were listed by the installed packages."
fi

section "Standalone packaged CSS state evidence"
for file in "${package_files[@]}"; do
  if [[ -r "$file" && ( "$file" == *.css || "$file" == *.scss ) ]]; then
    bounded_matches "$file" cat "$file"
  fi
done

section "Packaged GResource CSS state evidence"
if command -v gresource >/dev/null 2>&1; then
  found_gresource=0
  for file in "${package_files[@]}"; do
    if [[ -r "$file" && "$file" == *.gresource ]]; then
      found_gresource=1
      inspect_resource_container "Package resource" "$file"
    fi
  done
  if (( found_gresource == 0 )); then
    printf '%s\n' "No standalone .gresource package file found; checking ELF resource sections next."
  fi
else
  printf '%s\n' "gresource command unavailable; embedded CSS extraction skipped."
fi

section "Embedded Settings/libhandy GResource CSS state evidence"
if command -v readelf >/dev/null 2>&1 && command -v gresource >/dev/null 2>&1; then
  for file in "$SETTINGS_BIN" "$HANDY_LIB"; do
    [[ -n "$file" && -r "$file" ]] || continue
    sections=()
    mapfile -t sections < <(
      readelf -SW "$file" 2>/dev/null \
        | awk '$2 ~ /^\.gresource/ {print $2}'
    )
    if (( ${#sections[@]} == 0 )); then
      printf '%s\n' "No .gresource ELF section found in $file"
      continue
    fi
    for section_name in "${sections[@]}"; do
      inspect_resource_container "ELF resource" "$file" "$section_name"
    done
  done
else
  printf '%s\n' "readelf or gresource unavailable; ELF resource inspection skipped."
fi

section "Fallback binary strings"
for file in "$SETTINGS_BIN" "$HANDY_LIB"; do
  [[ -n "$file" && -r "$file" ]] || continue
  bounded_matches "$file" strings "$file"
done

section "Interpretation boundary"
printf '%s\n' "The target screenshot proves enabled Settings switches now render the GoreeCloud Mineral Teal track, while the Search navigation row still renders Zorin pale cyan."
printf '%s\n' "This diagnostic is intended to locate a Settings/libhandy CSS selector or higher-priority provider that can explain the remaining selected-row state before another styling change is attempted."
printf '%s\n' "Do not add broader theme overrides or change system theme locations based only on the absence of a resource match."

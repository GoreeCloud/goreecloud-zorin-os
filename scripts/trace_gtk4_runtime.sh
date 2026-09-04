#!/usr/bin/env bash
set -euo pipefail

# Focused, non-persistent GTK 4/libadwaita runtime-path trace for Zorin OS 17.3.
#
# This helper does not modify theme files, GTK configuration, packages, or
# system settings. It launches a temporary Settings process under strace and
# lets timeout stop that traced process after the observation window.

if ! command -v strace >/dev/null 2>&1; then
  echo "strace is not installed"
  exit 2
fi

if ! command -v gsettings >/dev/null 2>&1; then
  echo "gsettings is not available"
  exit 2
fi

if ! command -v gnome-control-center >/dev/null 2>&1; then
  echo "gnome-control-center is not available"
  exit 2
fi

active_theme="$(gsettings get org.gnome.desktop.interface gtk-theme 2>/dev/null | sed "s/^'//;s/'$//")"
if [[ -z "$active_theme" ]]; then
  echo "Unable to determine the active GTK theme"
  exit 2
fi

trace_file="$(mktemp -t goreecloud-gtk4-trace.XXXXXX)"
trap 'rm -f "$trace_file"' EXIT

user_theme_root="${XDG_DATA_HOME:-$HOME/.local/share}/themes/$active_theme"
system_theme_root="/usr/share/themes/$active_theme"

cat <<EOF
GoreeCloud GTK 4/libadwaita focused runtime trace
Active GTK theme: $active_theme
User-local theme root: $user_theme_root
System theme root: $system_theme_root

This helper writes only a temporary strace log and removes it on exit.
It does not change themes, GTK configuration, packages, or system settings.
EOF

# Avoid tracing an already-running Settings process, because launch-time theme
# provider lookup is the evidence we need. Do not terminate an existing process.
if pidof gnome-control-center >/dev/null 2>&1; then
  echo
  echo "gnome-control-center is already running. Close Settings completely, then rerun this helper."
  exit 3
fi

set +e
timeout 10s strace -f -qq \
  -e trace=execve,openat,newfstatat,readlinkat \
  -s 512 \
  -o "$trace_file" \
  gnome-control-center search >/dev/null 2>&1
trace_status=$?
set -e

# timeout normally returns 124 after the observation window. A clean early exit
# is also acceptable; other statuses are reported but do not discard evidence.
if [[ $trace_status -ne 0 && $trace_status -ne 124 ]]; then
  echo
  echo "Trace command exited with status $trace_status; showing captured evidence anyway."
fi

echo
echo "== Process execution evidence =="
exec_lines="$(grep -E 'execve\(' "$trace_file" || true)"
if [[ -n "$exec_lines" ]]; then
  printf '%s\n' "$exec_lines" | head -n 80
else
  echo "No execve lines captured."
fi

echo
echo "== Theme provider file-open/stat evidence =="
provider_lines="$(
  grep -E '(/usr/share/themes/|/home/[^\"]+/\.local/share/themes/|/gtk-4\.0/|/gtk-3\.0/|\.libadwaita)' "$trace_file" \
    | grep -v '/icons/' \
    | sed -E 's/^\[pid[[:space:]]+[0-9]+\][[:space:]]+//' \
    | awk '!seen[$0]++' \
    || true
)"
if [[ -n "$provider_lines" ]]; then
  printf '%s\n' "$provider_lines"
else
  echo "No theme-provider path activity matched the focused filter."
fi

path_seen() {
  local path="$1"
  if grep -Fq "$path" "$trace_file"; then
    echo "yes"
  else
    echo "no"
  fi
}

path_opened() {
  local path="$1"
  if grep -F "$path" "$trace_file" | grep -Eq '= [0-9]+$'; then
    echo "yes"
  else
    echo "no"
  fi
}

pattern_seen() {
  local pattern="$1"
  if grep -Eq "$pattern" "$trace_file"; then
    echo "yes"
  else
    echo "no"
  fi
}

echo
echo "== Focused summary =="
printf '%-52s %s\n' "user-local active-theme GTK 4 path seen:" "$(path_seen "$user_theme_root/gtk-4.0")"
printf '%-52s %s\n' "user-local active-theme GTK 4 file opened:" "$(path_opened "$user_theme_root/gtk-4.0")"
printf '%-52s %s\n' "system active-theme GTK 4 path seen:" "$(path_seen "$system_theme_root/gtk-4.0")"
printf '%-52s %s\n' "system active-theme GTK 4 file opened:" "$(path_opened "$system_theme_root/gtk-4.0")"
printf '%-52s %s\n' "user-local active-theme GTK 3 path seen:" "$(path_seen "$user_theme_root/gtk-3.0")"
printf '%-52s %s\n' "user-local active-theme GTK 3 file opened:" "$(path_opened "$user_theme_root/gtk-3.0")"
printf '%-52s %s\n' "system ZorinBlue GTK 4 path seen:" "$(pattern_seen '/usr/share/themes/ZorinBlue-(Light|Dark)/gtk-4\.0')"
printf '%-52s %s\n' "system ZorinBlue GTK 3 path seen:" "$(pattern_seen '/usr/share/themes/ZorinBlue-(Light|Dark)/gtk-3\.0')"
printf '%-52s %s\n' "any .libadwaita path seen:" "$(pattern_seen '\.libadwaita')"

echo
echo "Interpretation boundary:"
echo "- A successful open under the user-local active-theme gtk-4.0 directory means Settings/libadwaita did reach the GoreeCloud GTK 4 bytes; investigate later provider precedence instead of relocating the theme."
echo "- An attempted system active-theme gtk-4.0 path with no user-local GTK 4 access is evidence for a patched system-only lookup path."
echo "- GTK 3 activity alone is not sufficient to classify the Settings GTK 4/libadwaita provider path, especially when child processes are traced."
echo "- Do not copy the GoreeCloud theme into /usr/share/themes or populate ~/.config/gtk-4.0 based only on partial trace output."

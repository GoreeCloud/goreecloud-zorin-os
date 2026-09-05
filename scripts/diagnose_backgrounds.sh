#!/usr/bin/env bash
set -euo pipefail

echo "GoreeCloud Zorin stock-background audit"
echo "This helper is read-only. It does not delete, move, overwrite, install, or change wallpaper settings."
echo

echo "== Host / OS =="
hostnamectl --static 2>/dev/null || hostname
if [[ -r /etc/os-release ]]; then
  grep -E '^(NAME|ID|VERSION|VERSION_ID)=' /etc/os-release || true
fi
echo

echo "== Current user background settings =="
for key in picture-uri picture-uri-dark picture-options; do
  if gsettings list-keys org.gnome.desktop.background 2>/dev/null | grep -Fxq "$key"; then
    printf '%-18s %s\n' "$key" "$(gsettings get org.gnome.desktop.background "$key")"
  fi
done
echo

echo "== GNOME background-property catalogs =="
catalog_dir=/usr/share/gnome-background-properties
if [[ -d "$catalog_dir" ]]; then
  find "$catalog_dir" -maxdepth 1 -type f -name '*.xml' -print -exec ls -l -- {} \; | sort
else
  echo "Directory not present: $catalog_dir"
fi
echo

echo "== Catalog package ownership =="
if [[ -d "$catalog_dir" ]]; then
  while IFS= read -r file; do
    printf '\n-- %s --\n' "$file"
    dpkg-query -S "$file" 2>/dev/null || echo "unowned by dpkg"
  done < <(find "$catalog_dir" -maxdepth 1 -type f -name '*.xml' -print | sort)
fi
echo

echo "== Wallpaper roots =="
for dir in /usr/share/backgrounds /usr/share/wallpapers /usr/share/zorin-backgrounds; do
  if [[ -d "$dir" ]]; then
    printf '\n-- %s --\n' "$dir"
    find "$dir" -maxdepth 2 \( -type f -o -type l \) -printf '%p\t%k KiB\n' | sort
  fi
done
echo

echo "== Installed packages with background/wallpaper names =="
dpkg-query -W -f='${Package}\t${Version}\n' 2>/dev/null |
  grep -Ei '(^|[-])(background|wallpaper)s?($|[-])|zorin.*(background|wallpaper)' |
  sort || true
echo

echo "== Package ownership for wallpaper roots (bounded) =="
count=0
while IFS= read -r file; do
  count=$((count + 1))
  if (( count > 250 )); then
    echo "[stopped after 250 files]"
    break
  fi
  owner="$(dpkg-query -S "$file" 2>/dev/null | head -n1 || true)"
  printf '%s\t%s\n' "${owner:-unowned}" "$file"
done < <(find /usr/share/backgrounds /usr/share/wallpapers /usr/share/zorin-backgrounds \
  -xdev -type f 2>/dev/null | sort)
echo

echo "Audit complete."
echo "Do not delete stock wallpaper files yet. Use this output to define the exact recovery and replacement set."

#!/bin/bash
# Proves tests/apt-fallback.sh on a fake apt in a scratch folder. Run from anywhere: bash tests/test_apt_fallback.sh
# It touches nothing outside its scratch folders and needs no network. GitHub's checks run it before setup.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
fails=0
ok() { if eval "$2"; then echo "ok: $1"; else echo "FAIL: $1"; fails=$((fails + 1)); fi; }

# A stand-in for /etc/apt as GitHub's machines have it, and a fake apt that logs its calls, hangs while a source
# names a host in $SLOW_HOSTS and fails at once while a source names a host in $DOWN_HOSTS.
scratch() {
  D=$(mktemp -d); mkdir -p "$D/sources.list.d"
  printf 'http://azure.archive.ubuntu.com/ubuntu/\tpriority:1\nhttps://archive.ubuntu.com/ubuntu/\tpriority:2\nhttps://security.ubuntu.com/ubuntu/\tpriority:3\n' > "$D/apt-mirrors.txt"
  printf 'Types: deb\nURIs: mirror+file:/etc/apt/apt-mirrors.txt\nSuites: noble noble-updates\nComponents: main\n' > "$D/sources.list.d/ubuntu.sources"
  cat > "$D/apt" <<'EOF'
#!/bin/bash
echo "$*" >> "$APT_DIR/calls"
named() { grep -rqs "$1" "$APT_DIR/apt-mirrors.txt" "$APT_DIR/sources.list" "$APT_DIR/sources.list.d"; }
for h in $SLOW_HOSTS; do named "$h" && exec sleep 30; done
for h in $DOWN_HOSTS; do named "$h" && exit 100; done
exit 0
EOF
  chmod +x "$D/apt"
}
# fetch SLOW_HOSTS DOWN_HOSTS: run apt_fetch on the scratch folder with short limits; sets $code.
fetch() {
  (export APT_DIR="$D" APT="$D/apt" NO_SUDO=1 APT_UPDATE_TRY=1 APT_FIRST_TRY=1 APT_SECOND_TRY=2 SLOW_HOSTS="$1" DOWN_HOSTS="$2"
   . "$HERE/apt-fallback.sh"; apt_fetch poppler-utils) > "$D/out" 2> "$D/err"
  code=$?
}
azure_named() { grep -rqs azure.archive.ubuntu.com "$D/apt-mirrors.txt" "$D/sources.list" "$D/sources.list.d"; }

scratch; fetch "" ""
ok "a healthy mirror is used and left alone" '[ $code = 0 ] && azure_named && [ "$(wc -l < "$D/calls")" = 2 ]'
ok "apt prints nothing on standard output" '[ ! -s "$D/out" ]'

scratch; fetch "azure.archive.ubuntu.com" ""
ok "a mirror that hangs is given up and the archive fetched from" '[ $code = 0 ] && ! azure_named && grep -q archive.ubuntu.com "$D/apt-mirrors.txt"'
ok "the fetch is tried again after the mirror is taken out" 'tail -n 1 "$D/calls" | grep -q "install --download-only"'

scratch; fetch "" "azure.archive.ubuntu.com"
ok "a mirror that fails at once is given up too" '[ $code = 0 ] && ! azure_named'

scratch; fetch "azure.archive.ubuntu.com archive.ubuntu.com" ""
ok "every host hanging ends 2 and says it is the machine's fault" '[ $code = 2 ] && grep -q "fault of the machine" "$D/err"'

scratch; printf 'http://azure.archive.ubuntu.com/ubuntu/\tpriority:1\n' > "$D/apt-mirrors.txt"; fetch "azure.archive.ubuntu.com" ""
ok "a mirror list with no other host gains the archive" '[ $code = 0 ] && grep -q "http://archive.ubuntu.com/ubuntu/" "$D/apt-mirrors.txt"'

scratch; rm "$D/apt-mirrors.txt" "$D/sources.list.d/ubuntu.sources"; echo "deb http://azure.archive.ubuntu.com/ubuntu noble main" > "$D/sources.list"; fetch "azure.archive.ubuntu.com" ""
ok "a one-line list that names the mirror is pointed at the archive" '[ $code = 0 ] && grep -q "deb http://archive.ubuntu.com/ubuntu noble main" "$D/sources.list"'

scratch; printf 'https://archive.ubuntu.com/ubuntu/\tpriority:1\n' > "$D/apt-mirrors.txt"
ok "sources that do not name the mirror are told apart" '! (export APT_DIR="$D" NO_SUDO=1; . "$HERE/apt-fallback.sh"; names_azure)'

[ "$fails" = 0 ] && echo "all passed" || { echo "$fails failed"; exit 1; }

#!/bin/bash
# Fetch system packages without hanging on a slow package mirror. Sourced by tests/setup.sh.
#
# Why. GitHub's machines fetch from azure.archive.ubuntu.com, a mirror of Ubuntu's archive that is usually fast and at
# times slow or out of reach. apt stays on a slow mirror: its mirror list moves on only when a fetch fails outright,
# and its own time limits are long. On 19 November 2026 that turned a three-minute run into one of twenty, and then
# failed three runs in setup before any rule was checked.
#
# What it does. While apt's sources name that mirror, each read of the index and each fetch gets a time limit. If one
# runs out its time or fails, the mirror is taken out of apt's sources, so apt reads from archive.ubuntu.com, the
# archive's own host, and the step is tried once more. Packages are only fetched here (--download-only): installing
# them is left to the caller, with no limit, because a fetch cut short leaves the machine as it was and an install cut
# short would not. A fetch that fails on every host tried ends 2 and says it is the machine's fault, not the change's.
#
# The Mesmir repository's pipeline uses the same remedy. Only apt's own source files change, on a machine GitHub throws
# away after the run. Where the sources do not name the mirror, as in a working session, setup.sh does not call this.
# Its test is tests/test_apt_fallback.sh, which runs it on a fake apt in a scratch folder.

APT_DIR="${APT_DIR:-/etc/apt}"   # for the test: a scratch folder that stands in for /etc/apt
APT="${APT:-apt-get}"            # for the test: a fake apt
AZURE=azure.archive.ubuntu.com
ARCHIVE=archive.ubuntu.com
if [ "$(id -u)" = 0 ] || [ -n "${NO_SUDO:-}" ]; then AS_ROOT=(); else AS_ROOT=(sudo); fi

# apt's mirror lists: the image's own, and any that the source files name by "mirror+file:", in case the image moves it.
mirror_lists() {
  local f
  {
    printf '%s\n' "$APT_DIR/apt-mirrors.txt"
    grep -ohs 'mirror+file:/[^[:space:]]*' "$APT_DIR/sources.list" "$APT_DIR"/sources.list.d/* 2>/dev/null \
      | sed "s|^mirror+file:||; s|^/etc/apt/|$APT_DIR/|"
  } | sort -u | while read -r f; do [ -f "$f" ] && printf '%s\n' "$f"; done
  return 0
}

# apt's other source files: the one-line lists and the deb822 lists.
source_lists() {
  local f
  for f in "$APT_DIR/sources.list" "$APT_DIR"/sources.list.d/*.list "$APT_DIR"/sources.list.d/*.sources; do
    [ -f "$f" ] && printf '%s\n' "$f"
  done
  return 0
}

# Whether any of apt's source files still names the Azure mirror.
names_azure() {
  local f
  for f in $(mirror_lists) $(source_lists); do
    grep -q "$AZURE" "$f" && return 0
  done
  return 1
}

# Take the Azure mirror out of every source file that names it. In a mirror list its line is dropped, since the next
# line is the archive's own host, which is added where the list has none. In any other file its name gives way to the
# archive's, so the field that names it is kept whole.
leave_azure() {
  local f
  for f in $(mirror_lists); do
    grep -q "$AZURE" "$f" || continue
    "${AS_ROOT[@]}" sed -i "/$AZURE/d" "$f"
    grep -q "$ARCHIVE" "$f" || printf 'http://%s/ubuntu/\tpriority:1\n' "$ARCHIVE" | "${AS_ROOT[@]}" tee -a "$f" >/dev/null
    echo "setup: took $AZURE out of $f" >&2
  done
  for f in $(source_lists); do
    grep -q "$AZURE" "$f" || continue
    "${AS_ROOT[@]}" sed -i "s/$AZURE/$ARCHIVE/g" "$f"
    echo "setup: took $AZURE out of $f" >&2
  done
}

# limited SECONDS COMMAND...: run COMMAND as root with a time limit. The limit is kept by coreutils' timeout, itself
# run as root, so that a stopped apt lets go of its lock.
limited() {
  local seconds=$1; shift
  "${AS_ROOT[@]}" timeout -k 10 "$seconds" "$@"
}

# apt_fetch PACKAGE...: read apt's index and fetch the packages, falling back from the Azure mirror once.
# What apt prints goes to standard error, so that setup.sh's last line of output stays the one its caller reads.
apt_fetch() {
  [ $# -gt 0 ] || return 0
  local get=(install --download-only -y -q --no-install-recommends "$@")
  if names_azure; then
    if limited "${APT_UPDATE_TRY:-60}" "$APT" update -q >&2 && limited "${APT_FIRST_TRY:-120}" "$APT" "${get[@]}" >&2; then
      return 0
    fi
    echo "setup: apt's index or the fetch failed or ran out its time on $AZURE: trying $ARCHIVE" >&2
    leave_azure
  fi
  if limited "${APT_SECOND_TRY:-300}" "$APT" update -q >&2 && limited "${APT_SECOND_TRY:-300}" "$APT" "${get[@]}" >&2; then
    return 0
  fi
  echo "setup: FAIL: apt could not fetch its packages from any host tried. This is a fault of the machine's package mirror, not of the change." >&2
  return 2
}

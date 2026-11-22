# Checks

`SPEC.md` is the design spec: numbered rules the site must meet. `check_site.py` builds the site and checks every rule marked **auto**, then writes `report.md` and exits with an error if any rule fails. `mutations.sh` breaks copies of the site on purpose, a hundred and two ways, to prove the checks catch real regressions.

## Run

1. Install once: Hugo 0.141.0 extended, Python 3 with `playwright` (1.42 or later, for tagged PDFs), `pyyaml`, `Pillow`, `numpy`, `beautifulsoup4`, `pikepdf` and `pypdfium2`, Chrome, `pdftotext` and `pdfinfo` (poppler), `npm install --prefix tests` for axe-core, and `python3 -m playwright install webkit firefox` for rule R8.
2. From the repo root: `HUGO=/path/to/hugo python3 tests/check_site.py`. Point `CHROME` at a Chrome or Chromium binary if it is not on the path.
3. Read `tests/report.md`. Every failure names its rule.

Rules A5 to A12 and P4 came from the round 7 accessibility review. Round 8 added the type and spacing scales (T4 to T8, W4), enlarged text and custom text spacing (R7, A13), the WebKit and Firefox runs (R8) and folded source reasons (S4). Round 10 locked the look: V2 (one look, no switches) and the round 9 baseline for V1, which runs in working sessions; GitHub's checks run everything else with `--skip V1`. `setup.sh` installs everything below on Linux. Round 9 added the owner's margin-note slots (M4, and M1 to M3 rewritten), letters wholly on the highlighter (C6), varied hand-drawn marks (H1), and the self-contained, bookmarked PDF with its metadata (P5, P6). The margin rules run on a second build with a sample note in every slot, so they are checked with notes present. Round 1 of the rebuilds (21 November 2026) added the owner's editing pass: his own first-person sentences listed for E3, source entries as recommendations (S13), times rounded his way (S14), notes beside the paragraph they name (M1 to M4), and a fourth printed page for a module's full path (P1). `--only` runs just the checks behind the rules you name. A4 (a screen reader pass) still needs a person: the review read Chrome's accessibility tree, which is what screen readers read, but no one has yet listened with VoiceOver or NVDA.

## Setup on GitHub's machines

`setup.sh` fetches system packages through `apt-fallback.sh`. GitHub's machines read from a package mirror that is at times slow or out of reach, so each fetch gets a time limit and falls back to `archive.ubuntu.com`. `test_apt_fallback.sh` proves it on a fake apt, and GitHub's checks run that test before setup. A working session's apt is left as it is.

## The working source (X1 to X3) and the voice (E1 to E3, S5, S7)

`tools-pm/source-doc.py` makes the working doc's tabs from the repository: a built unit from its built page, a draft from its file in `drafts/pm/`. The checks read those same tabs. X1 holds one source for every module on the map. X2 compares each built page's words with its tab. X3 compares each tab with `tools-pm/source-doc.lock.json`, the record of what was last put in the doc, and fails until the doc is synced and the record updated. E1 to E3 hold the voice (`VOICE.md`), S5 keeps the settings in `retired-settings.txt` out of the examples, and S7 keeps a "To check:" line out of a built unit.

## Rules for changes

- Change `SPEC.md` first, then the site, then the check. A change that makes a check fail is not done.
- Record a new visual baseline (`--update-baseline`) only after the owner approves the look. Until then, rule V1 only notes that no baseline exists.

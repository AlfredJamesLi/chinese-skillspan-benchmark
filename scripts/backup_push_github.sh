#!/usr/bin/env bash
# Snapshot new run_summary files and push the private GitHub backup.
# Usage: bash scripts/backup_push_github.sh "short why"
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
PAPER="/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper"
MSG="${1:-Update paper result snapshots}"
cd "$PAPER"

python3 "$PAPER/scripts/build_max_tables.py" || true

# copy any new run_summary.json into results_snapshots
python3 - << 'PY'
from pathlib import Path
PAPER = Path("/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper")
snap = PAPER / "results_snapshots"
snap.mkdir(exist_ok=True)
copied = []
for p in PAPER.joinpath("output").rglob("run_summary.json"):
    rel = p.relative_to(PAPER / "output").parent.as_posix().replace("/", "__")
    dest = snap / f"{rel}.json"
    if (not dest.exists()) or dest.read_bytes() != p.read_bytes():
        dest.write_bytes(p.read_bytes())
        copied.append(dest.name)
print("copied", len(copied), "snapshots")
PY

git add paper_results tables results_snapshots README.md scripts notes HANDOFF.md PUSH_GITHUB.md REPRO_GITHUB.md data/LARGE_DATA_MANIFEST.md data/*sents.meta.json 2>/dev/null || true
if git diff --cached --quiet; then
  echo "[backup] nothing to commit"
  exit 0
fi
git -c user.email="guojingli3@users.noreply.github.com" -c user.name="guojingli3" commit -m "$MSG"
gh auth setup-git >/dev/null 2>&1 || true
git push origin main
echo "[backup] pushed $(git rev-parse --short HEAD)"

#!/usr/bin/env python3
"""Local validator for public-release docs. Not part of the Zenodo deposit."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

PAPER = Path(__file__).resolve().parents[1]
errors: list[str] = []

EXPECTED_AUTHORS_CFF = [
    ("Guojing", "Li"),
    ("Zichuan", "Fu"),
    ("Junyi", "Li"),
    ("Wenlin", "Zhang"),
    ("Kaifeng", "Guo"),
    ("Jinning", "Yang"),
    ("Jingtong", "Gao"),
    ("Xiangyu", "Zhao"),
]
TITLE = "Chinese-SkillSpan: A Benchmark for Competency Span Extraction from Chinese Job Advertisements"

p = PAPER / "release/zenodo/.zenodo.json"
data = json.loads(p.read_text())
names = [c["name"] for c in data["creators"]]
expected_z = [
    "Li, Guojing",
    "Fu, Zichuan",
    "Li, Junyi",
    "Zhang, Wenlin",
    "Guo, Kaifeng",
    "Yang, Jinning",
    "Gao, Jingtong",
    "Zhao, Xiangyu",
]
if names != expected_z:
    errors.append(f"zenodo creator order {names}")
print("OK JSON .zenodo.json")

cff_text = (PAPER / "CITATION.cff").read_text()
if yaml is None:
    print("WARN: PyYAML missing; CFF/front-matter schema not fully checked")
else:
    c = yaml.safe_load(cff_text)
    if c.get("title") != TITLE:
        errors.append(f"CFF title {c.get('title')!r}")
    got = [(a.get("given-names"), a.get("family-names")) for a in c.get("authors", [])]
    if got != EXPECTED_AUTHORS_CFF:
        errors.append(f"CFF authors {got}")
    print("OK CFF YAML", "cff-version", c.get("cff-version"))

    for rel in (
        "release/huggingface-model/README.md",
        "release/huggingface-dataset/README.md",
    ):
        raw = (PAPER / rel).read_text()
        if not raw.startswith("---\n"):
            errors.append(f"{rel}: missing front matter")
            continue
        parts = raw.split("---\n", 2)
        if len(parts) < 3:
            errors.append(f"{rel}: front matter not closed")
            continue
        meta = yaml.safe_load(parts[1])
        if meta.get("license") != "other":
            errors.append(f"{rel} license {meta.get('license')}")
        print("OK YAML", rel)

md_files = [
    "README.md",
    "REPRODUCIBILITY.md",
    "DATA_AVAILABILITY.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "docs/RELEASE_CHECKLIST.md",
    "release/huggingface-model/README.md",
    "release/huggingface-dataset/README.md",
    "release/zenodo/README.md",
    "release/zenodo/RELEASE_MANIFEST.md",
]
link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
for rel in md_files:
    src = PAPER / rel
    for m in link_re.finditer(src.read_text()):
        url = m.group(2).split()[0]
        if url.startswith(("http://", "https://", "mailto:", "#", "[TODO")):
            continue
        target = (src.parent / url.split("#")[0]).resolve()
        if not target.exists():
            errors.append(f"broken link in {rel}: {url}")

todo_re = re.compile(r"\[TODO:[^\]]+\]")
print("\n===== TODO items =====")
n = 0
for rel in sorted(md_files + ["CITATION.cff", "release/zenodo/.zenodo.json"]):
    for t in todo_re.findall((PAPER / rel).read_text()):
        n += 1
        print(f"{rel}: {t}")
print("TODO count", n)

print("\n===== hashes =====")
for rel in md_files + ["CITATION.cff", "release/zenodo/.zenodo.json"]:
    path = PAPER / rel
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"{path.stat().st_size}\t{digest}\t{rel}")

if errors:
    print("\nERRORS")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("\nNo structural errors")

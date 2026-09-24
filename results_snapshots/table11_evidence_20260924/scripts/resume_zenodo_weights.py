#!/usr/bin/env python3
"""Resume draft 22937245: upload six model.safetensors with Content-Length, then publish."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
EV = ROOT / "TABLE11_EVIDENCE_20260924"
TOKEN = Path("/home/guojingli3/.zenodo_token").read_text().strip()
API = "https://zenodo.org/api"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
DEP_ID = 22937245
FORBIDDEN_IDS = {22288338, 22288337, 22685143, 22698504, 22846011, 22851581}

CELLS = [
    ("xlm-roberta-large", 42),
    ("xlm-roberta-large", 43),
    ("xlm-roberta-large", 44),
    ("esco-xlm-roberta-large", 42),
    ("esco-xlm-roberta-large", 43),
    ("esco-xlm-roberta-large", 44),
]


def raise_for(r, ctx):
    if r.status_code >= 400:
        raise SystemExit(f"{ctx}: HTTP {r.status_code} {r.text[:500]}")


def list_names(dep):
    names = set()
    for f in dep.get("files") or []:
        names.add(f.get("filename") or f.get("key"))
    return names


def upload_fixed_length(bucket: str, path: Path, name: str) -> None:
    size = path.stat().st_size
    url = f"{bucket}/{quote(name)}"
    print(f"[upload] {name} {size} bytes", flush=True)
    hdr = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(size),
    }
    last_err = None
    for attempt in range(1, 4):
        with path.open("rb") as fp:
            r = requests.put(url, data=fp, headers=hdr, timeout=None)
        if r.status_code < 400:
            print(f"[ok] {name} attempt={attempt} http={r.status_code}", flush=True)
            return
        last_err = f"HTTP {r.status_code} {r.text[:300]}"
        print(f"[retry] {name} attempt={attempt} {last_err}", flush=True)
    raise SystemExit(f"upload failed {name}: {last_err}")


def main() -> int:
    assert DEP_ID not in FORBIDDEN_IDS
    r = requests.get(f"{API}/deposit/depositions/{DEP_ID}", headers=HEADERS, timeout=60)
    raise_for(r, "get draft")
    dep = r.json()
    assert dep["state"] == "unsubmitted"
    bucket = dep["links"]["bucket"]
    have = list_names(dep)
    print("[have]", sorted(have), flush=True)
    for short, seed in CELLS:
        name = f"cnss_table11_{short}_s{seed}_model.safetensors"
        if name in have:
            print(f"[skip] {name}", flush=True)
            continue
        src = ROOT / "runs" / "chinese" / "full" / short / str(seed) / "best" / "model.safetensors"
        upload_fixed_length(bucket, src, name)
    # reload then metadata+publish using the already written metadata helper
    from upload_table11_zenodo import metadata

    meta_r = requests.put(
        f"{API}/deposit/depositions/{DEP_ID}",
        json={"metadata": metadata()},
        headers=HEADERS,
        timeout=60,
    )
    raise_for(meta_r, "metadata")
    pub = requests.post(f"{API}/deposit/depositions/{DEP_ID}/actions/publish", headers=HEADERS, timeout=180)
    raise_for(pub, "publish")
    rec = pub.json()
    out = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "deposition_id": DEP_ID,
        "doi": rec.get("doi") or (rec.get("metadata") or {}).get("doi"),
        "concept_doi": rec.get("conceptdoi") or (rec.get("metadata") or {}).get("conceptdoi"),
        "url": rec.get("links", {}).get("html"),
        "state": rec.get("state"),
        "n_files": len(rec.get("files") or []),
        "forbidden_ids_untouched": sorted(FORBIDDEN_IDS),
    }
    (EV / "zenodo_publish_receipt.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

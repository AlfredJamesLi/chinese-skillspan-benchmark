#!/usr/bin/env python3
"""Create a NEW Zenodo record for Table 11 LSKT checkpoints. Never touch v0.1.x records."""
from __future__ import annotations

import json
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
EV = ROOT / "TABLE11_EVIDENCE_20260924"
STAGING = Path("/tmp/cnss_table11_zenodo")
TOKEN = Path("/home/guojingli3/.zenodo_token").read_text().strip()
API = "https://zenodo.org/api"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
FORBIDDEN_IDS = {
    22288338,
    22288337,
    22685143,
    22698504,
    22846011,
    22851581,
}

CELLS = [
    ("xlm-roberta-large", 42, "c894df3762a57fd8c10af65a2745db33d94f8aa4476fb4077a9615b1de6ef1f5", 0.49957662997459773, 11, "0c6cc1999f5dec727eec4d682a04e2da947775a9"),
    ("xlm-roberta-large", 43, "be3caa3ed3a7ebf5a6ffe3d698440bc15c0b4fb8dd856157e74a47ee45fded49", 0.5224489795918368, 14, "ce98c854fc5a367ff36e837c83a94c5afa22b932"),
    ("xlm-roberta-large", 44, "8946f8cfe5ed772da6d9d97886f2bd1b86be748dc6209d3c9bd1d98d6121b6e3", 0.5445705024311183, 14, "d0f29363f644f0e0835f1291d295caf468b368b9"),
    ("esco-xlm-roberta-large", 42, "8d44b7f25de2cebe33a273a6caaf1aebc3076032d3d0fb0eceadb552bf9bc05f", 0.5160758450123661, 19, "af5d4716f682f8d53ebda464b301deffa2adee16"),
    ("esco-xlm-roberta-large", 43, "2efb6f69def4211a07a9ad30ee4563fe0dd83569d7e3687676b9077be6acc3aa", 0.5401459854014599, 15, "45e1fae014a21c738b4f727ba34b2f5c80324bfc"),
    ("esco-xlm-roberta-large", 44, "98ce01afc2a13fad9cd7db1458c55332df23651d4ce84f6a4d9c653d5b9c9524", 0.5576763485477179, 10, "55a0149ea5dda2ecafb0564c0c3368d1afa7f07a"),
]


def hf_id(short, seed):
    return f"AlfredJames/cnss-table11-lskt-{short}-b2-s{seed}"


def raise_for(r: requests.Response, ctx: str) -> None:
    if r.status_code >= 400:
        raise SystemExit(f"{ctx}: HTTP {r.status_code} {r.text[:800]}")


def metadata() -> dict:
    related = [
        {"identifier": "https://github.com/AlfredJamesLi/chinese-skillspan-benchmark", "relation": "isSupplementTo", "resource_type": "software", "scheme": "url"},
        {"identifier": "https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/audit/table11-evidence-20260924/results_snapshots/table11_evidence_20260924", "relation": "isDocumentedBy", "resource_type": "other", "scheme": "url"},
        {"identifier": "10.5281/zenodo.22698504", "relation": "references", "resource_type": "dataset", "scheme": "doi"},
        {"identifier": "10.5281/zenodo.22288337", "relation": "references", "resource_type": "dataset", "scheme": "doi"},
    ]
    for short, seed, *_rest in CELLS:
        related.append(
            {
                "identifier": f"https://huggingface.co/{hf_id(short, seed)}",
                "relation": "isIdenticalTo",
                "resource_type": "software",
                "scheme": "url",
            }
        )
    desc = """<p>This is an <strong>additional</strong> archive of six Chinese LSKT linear-head checkpoints used for Chinese-SkillSpan Table 11 / <code>tab:external-chinese</code>. It is <strong>not</strong> a new version of the Chinese-SkillSpan dataset DOIs (v0.1.1 <code>10.5281/zenodo.22288338</code>, v0.1.2 <code>10.5281/zenodo.22685143</code>, v0.1.3 <code>10.5281/zenodo.22698504</code>, concept <code>10.5281/zenodo.22288337</code>) and it is <strong>not</strong> JobBERT-zh CRF.</p>
<p>Protocol: new <code>XLMRobertaForTokenClassification</code> head on Silver-plus B2 (2,150 train / 169 dev), seeds 42/43/44, float32, encoder not frozen. Gold150 (SHA-256 <code>ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0</code>) is a frozen human-reference diagnostic set, not a new blind test. Scorer: <code>cnss-lskt-1.2.0</code> typed exact micro-F1.</p>
<p>Canonical load path is Hugging Face (byte-identical weights). This Zenodo record stores the same <code>model.safetensors</code> files plus the lightweight Table 11 evidence pack.</p>
<ul>
<li>XLM-R-large mean ± sample SD: <strong>0.522 ± 0.022</strong></li>
<li>ESCOXLM-R mean ± sample SD: <strong>0.538 ± 0.021</strong></li>
</ul>
<p>Per-seed typed exact: XLM-R 0.499577 / 0.522449 / 0.544571 (epochs 11/14/14); ESCO 0.516076 / 0.540146 / 0.557676 (epochs 19/15/10).</p>
<p>Hub: <a href="https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s42">s42</a>, <a href="https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s43">s43</a>, <a href="https://huggingface.co/AlfredJames/cnss-table11-lskt-xlm-roberta-large-b2-s44">s44</a>, <a href="https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s42">ESCO s42</a>, <a href="https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s43">ESCO s43</a>, <a href="https://huggingface.co/AlfredJames/cnss-table11-lskt-esco-xlm-roberta-large-b2-s44">ESCO s44</a>.</p>
<p>Evidence: <a href="https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/tree/audit/table11-evidence-20260924/results_snapshots/table11_evidence_20260924">GitHub audit pack</a>. Code: <a href="https://github.com/AlfredJamesLi/chinese-skillspan-benchmark">chinese-skillspan-benchmark</a>. Equal contribution: Guojing Li and Zichuan Fu. Corresponding author: Xiangyu Zhao (xianzhao@cityu.edu.hk). Grant No. 21BGL142.</p>"""
    return {
        "title": "Chinese-SkillSpan Table 11 LSKT linear-head checkpoints (XLM-R and ESCOXLM-R, B2, three seeds)",
        "upload_type": "software",
        "description": desc,
        "creators": [
            {"name": "Li, Guojing", "affiliation": "Renmin University of China; City University of Hong Kong"},
            {"name": "Fu, Zichuan", "affiliation": "City University of Hong Kong"},
            {"name": "Li, Junyi", "affiliation": "City University of Hong Kong"},
            {"name": "Zhang, Wenlin", "affiliation": "City University of Hong Kong"},
            {"name": "Guo, Kaifeng", "affiliation": "City University of Hong Kong"},
            {"name": "Yang, Jinning", "affiliation": "City University of Hong Kong"},
            {"name": "Gao, Jingtong", "affiliation": "City University of Hong Kong"},
            {"name": "Zhao, Xiangyu", "affiliation": "City University of Hong Kong"},
        ],
        "keywords": [
            "Chinese-SkillSpan",
            "LSKT",
            "skill span extraction",
            "XLM-RoBERTa",
            "ESCOXLM-R",
            "Table 11",
        ],
        "access_right": "open",
        "license": "other-closed",
        "version": "table11-lskt-20260924",
        "notes": "NEW record, not a version of 10.5281/zenodo.22288337. Do not overwrite v0.1.1 (22288338), v0.1.2 (22685143), v0.1.3 (22698504), Qwen adapters (22851581), or dataset record 22846011. Canonical serving URL is Hugging Face; this deposit archives the same weights. Licence other-closed to match Hub cards (license: other). Grant 21BGL142.",
        "related_identifiers": related,
        "language": "eng",
    }


def write_deposit_readme() -> Path:
    STAGING.mkdir(parents=True, exist_ok=True)
    p = STAGING / "README.md"
    lines = [
        "# Chinese-SkillSpan Table 11 LSKT linear-head checkpoints",
        "",
        "This Zenodo record is an **additional archive**. It does **not** replace dataset DOIs v0.1.1–v0.1.3.",
        "Load from Hugging Face unless you need a DOI snapshot of the weights.",
        "",
        "| File prefix | Encoder | Seed | Gold150 typed exact | Hugging Face |",
        "|---|---|---:|---:|---|",
    ]
    for short, seed, wsha, f1, ep, _c in CELLS:
        lines.append(
            f"| `cnss_table11_{short}_s{seed}_` | {short} | {seed} | {f1:.6f} | https://huggingface.co/{hf_id(short, seed)} |"
        )
    lines += [
        "",
        "Each seed has `*_model.safetensors` (SHA-256 in `WEIGHTS_SHA256.txt`) and `*_sidecar.tar` (config, tokenizer, model card).",
        "`table11_evidence_20260924.zip` is the lightweight audit pack (no 2 GiB weights).",
        "",
        "Gold150 freeze SHA-256: `ca8db0bc386c24543fec845d42ea8e24883eb67b8ce75129ac1768c5c0310fd0`.",
    ]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    sha_p = STAGING / "WEIGHTS_SHA256.txt"
    sha_p.write_text(
        "\n".join(f"{wsha}  cnss_table11_{short}_s{seed}_model.safetensors" for short, seed, wsha, *_ in CELLS) + "\n",
        encoding="utf-8",
    )
    return p


def zip_evidence() -> Path:
    out = STAGING / "table11_evidence_20260924.zip"
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in sorted(EV.rglob("*")):
            if not f.is_file():
                continue
            z.write(f, f.relative_to(EV.parent))
    return out


def sidecar(short: str, seed: int) -> Path:
    best = ROOT / "runs" / "chinese" / "full" / short / str(seed) / "best"
    card = EV / "model_cards" / f"{short}_s{seed}.md"
    out = STAGING / f"cnss_table11_{short}_s{seed}_sidecar.tar"
    with tarfile.open(out, "w") as tar:
        for name in ("config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "sentencepiece.bpe.model"):
            tar.add(best / name, arcname=name)
        tar.add(card, arcname="README.md")
    return out


def upload(bucket: str, path: Path, name: str | None = None) -> dict:
    name = name or path.name
    url = f"{bucket}/{quote(name)}"
    print(f"[upload] {name} ({path.stat().st_size} bytes)", flush=True)
    with path.open("rb") as fp:
        r = requests.put(url, data=fp, headers=HEADERS, timeout=None)
    raise_for(r, f"upload {name}")
    return r.json() if r.text else {"filename": name}


def main() -> int:
    write_deposit_readme()
    evzip = zip_evidence()
    sidecars = [sidecar(s, seed) for s, seed, *_ in CELLS]
    print("[create] new deposition", flush=True)
    r = requests.post(f"{API}/deposit/depositions", json={}, headers=HEADERS, timeout=60)
    raise_for(r, "create")
    dep = r.json()
    dep_id = dep["id"]
    if dep_id in FORBIDDEN_IDS:
        raise SystemExit(f"refusing forbidden id {dep_id}")
    bucket = dep["links"]["bucket"]
    print(f"[draft] id={dep_id} bucket={bucket}", flush=True)
    uploaded = []
    for path in [STAGING / "README.md", STAGING / "WEIGHTS_SHA256.txt", evzip, *sidecars]:
        uploaded.append(upload(bucket, path))
    for short, seed, wsha, *_ in CELLS:
        src = ROOT / "runs" / "chinese" / "full" / short / str(seed) / "best" / "model.safetensors"
        uploaded.append(upload(bucket, src, f"cnss_table11_{short}_s{seed}_model.safetensors"))
    meta_r = requests.put(
        f"{API}/deposit/depositions/{dep_id}",
        json={"metadata": metadata()},
        headers=HEADERS,
        timeout=60,
    )
    raise_for(meta_r, "metadata")
    pub = requests.post(f"{API}/deposit/depositions/{dep_id}/actions/publish", headers=HEADERS, timeout=120)
    raise_for(pub, "publish")
    rec = pub.json()
    doi = rec.get("doi") or (rec.get("metadata") or {}).get("doi")
    html = rec.get("links", {}).get("html")
    out = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "deposition_id": dep_id,
        "doi": doi,
        "url": html,
        "concept_doi": rec.get("conceptdoi") or (rec.get("metadata") or {}).get("conceptdoi"),
        "state": rec.get("state"),
        "forbidden_ids_untouched": sorted(FORBIDDEN_IDS),
        "n_files_uploaded": len(uploaded),
    }
    (EV / "zenodo_publish_receipt.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

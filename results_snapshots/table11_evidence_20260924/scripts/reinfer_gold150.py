#!/usr/bin/env python3
"""Re-infer Gold150 from the six frozen Table-11 checkpoints. No training, no gold-tag input."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
EV = ROOT / "TABLE11_EVIDENCE_20260924"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "adapters"))
from convert_gold150_to_bio import convert_record  # noqa: E402
from run_chinese_encoder import LSKT_LABELS, encode_keep_words  # noqa: E402
from score_lskt import score as official_score  # noqa: E402

CELLS = [
    ("xlm-roberta-large", 42),
    ("xlm-roberta-large", 43),
    ("xlm-roberta-large", 44),
    ("esco-xlm-roberta-large", 42),
    ("esco-xlm-roberta-large", 43),
    ("esco-xlm-roberta-large", 44),
]


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> int:
    import torch
    from transformers import AutoModelForTokenClassification, AutoTokenizer, DataCollatorForTokenClassification

    gold_raw = read_jsonl(ROOT / "chinese_data" / "gold150_test.jsonl")
    gold_bio = [convert_record(r) for r in gold_raw]
    device = torch.device("cuda")
    assert device.type == "cuda"
    out_root = EV / "reinfer_20260924"
    out_root.mkdir(parents=True, exist_ok=True)
    summary = []
    for short, seed in CELLS:
        run = ROOT / "runs" / "chinese" / "full" / short / str(seed)
        best = run / "best"
        old_pred = read_jsonl(run / "gold150_predictions.jsonl")
        dest = out_root / short / str(seed)
        dest.mkdir(parents=True, exist_ok=True)
        tokenizer = AutoTokenizer.from_pretrained(best, use_fast=True)
        model = AutoModelForTokenClassification.from_pretrained(best).to(device)
        model.eval()
        labels = list(LSKT_LABELS)
        ids = {t: i for i, t in enumerate(labels)}
        limit = min(512, int(getattr(model.config, "max_position_embeddings", 512)) - 2)
        rows = [{"id": r["id"], "tokens": r["tokens"], "tags": ["O"] * len(r["tokens"]), "sentence": r["sentence"]} for r in gold_bio]
        pieces, meta = [], []
        for row, r in enumerate(rows):
            start = 0
            while start < len(r["tokens"]):
                stop = min(start + 128, len(r["tokens"]))
                chunk = list(r["tokens"][start:stop])
                while True:
                    encoded, first, _replaced = encode_keep_words(tokenizer, chunk)
                    if len(encoded["input_ids"]) <= limit:
                        break
                    assert len(chunk) > 1
                    chunk = chunk[: len(chunk) // 2]
                    stop = start + len(chunk)
                assert set(first) == set(range(stop - start))
                encoded["labels"] = [-100] * len(encoded["input_ids"])
                for w, pos in first.items():
                    encoded["labels"][pos] = ids[r["tags"][start + w]]
                pieces.append(dict(encoded))
                meta.append((row, start, stop, first))
                start = stop
        collator = DataCollatorForTokenClassification(tokenizer)
        loader = torch.utils.data.DataLoader(pieces, batch_size=8, shuffle=False, collate_fn=collator)
        pred = [["O"] * len(r["tokens"]) for r in rows]
        cursor = 0
        with torch.no_grad():
            for batch in loader:
                outputs = model(**{k: v.to(device) for k, v in batch.items() if k != "labels"}).logits.argmax(-1).cpu().tolist()
                for output in outputs:
                    row, start, stop, first = meta[cursor]
                    cursor += 1
                    for w, pos in first.items():
                        pred[row][start + w] = labels[output[pos]]
        assert cursor == len(meta)
        pred_path = dest / "gold150_predictions.reinfer.jsonl"
        with pred_path.open("w", encoding="utf-8") as f:
            for i, tags in enumerate(pred):
                f.write(json.dumps({"id": gold_bio[i]["id"], "list_of_selection_bio4": tags, "tokens": gold_bio[i]["tokens"]}, ensure_ascii=False) + "\n")
        n_tag_diff = sum(1 for a, b in zip(old_pred, pred) if a["list_of_selection_bio4"] != b)
        n_id_diff = sum(1 for a, b in zip(old_pred, gold_bio) if a["id"] != b["id"])
        gold_bio_path = run / "gold150_gold.bio.jsonl"
        official = official_score(str(gold_bio_path), str(pred_path), align_mode="official", n_boot=2000, boot_seed=20260921)
        (dest / "gold150_official.reinfer.json").write_text(json.dumps(official, indent=2, default=str), encoding="utf-8")
        rec = {
            "encoder": short,
            "seed": seed,
            "checkpoint": str(best),
            "n_sentences": len(pred),
            "n_rows_with_tag_diff_vs_frozen_pred": n_tag_diff,
            "n_id_order_diff": n_id_diff,
            "typed_exact_f1_reinfer": official["typed_exact"]["f1"],
            "typed_exact_f1_old": json.loads((run / "gold150_official.json").read_text())["typed_exact"]["f1"],
            "gpu": torch.cuda.get_device_name(0),
            "torch": torch.__version__,
        }
        rec["exact_f1_equal"] = rec["typed_exact_f1_reinfer"] == rec["typed_exact_f1_old"]
        (dest / "compare.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
        summary.append(rec)
        del model
        torch.cuda.empty_cache()
        print(json.dumps(rec), flush=True)
    (out_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

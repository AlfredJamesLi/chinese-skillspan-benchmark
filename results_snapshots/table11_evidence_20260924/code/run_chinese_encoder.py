#!/usr/bin/env python3
"""Chinese LSKT linear-head baseline. New output layer; not JobBERT-zh CRF and not English-head transfer."""
from pathlib import Path
import argparse, json, hashlib, random, platform, time, sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "adapters"))
from convert_gold150_to_bio import convert_record, FREEZE_SHA256  # noqa: E402
from score_lskt import score as official_score  # noqa: E402

LSKT_LABELS = ["B-K", "B-L", "B-S", "B-T", "I-K", "I-L", "I-S", "I-T", "O"]
PLACEHOLDER = "■"


def encode_keep_words(tokenizer, words):
    words = list(words)
    for i, w in enumerate(words):
        if w is None or w == "" or w.isspace() or any(ord(c) < 32 for c in w):
            words[i] = PLACEHOLDER
    encoded = tokenizer(words, is_split_into_words=True, truncation=False)
    first = {}
    for pos, w in enumerate(encoded.word_ids()):
        if w is not None and w not in first:
            first[w] = pos
    missing = sorted(set(range(len(words))) - set(first))
    for i in missing:
        words[i] = PLACEHOLDER
    encoded = tokenizer(words, is_split_into_words=True, truncation=False)
    first = {}
    for pos, w in enumerate(encoded.word_ids()):
        if w is not None and w not in first:
            first[w] = pos
    return encoded, first, missing


def arguments():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", required=True)
    p.add_argument("--revision", required=True)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--smoke", action="store_true")
    p.add_argument("--train", type=Path, default=ROOT / "chinese_data" / "train_b2.jsonl")
    p.add_argument("--dev", type=Path, default=ROOT / "chinese_data" / "dev_b2.jsonl")
    p.add_argument("--gold150", type=Path, default=ROOT / "chinese_data" / "gold150_test.jsonl")
    return p.parse_args()


def read_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entities(tags):
    out = []
    start = None
    kind = None
    for i, t in enumerate(list(tags) + ["O"]):
        prefix = t.split("-", 1)[0]
        typ = t.split("-", 1)[1] if "-" in t else "SPAN"
        if start is not None and (prefix not in ("I", "E") or typ != kind):
            out.append((start, i, kind))
            start = None
        if prefix in ("B", "S") or (prefix in ("I", "E") and start is None):
            start = i
            kind = typ
        if prefix in ("S", "E") and start is not None:
            out.append((start, i + 1, kind))
            start = None
    return set(out)


def span_f1(gold, pred):
    tp = sum(len(g & p) for g, p in zip(gold, pred))
    ng = sum(map(len, gold))
    np_ = sum(map(len, pred))
    return {
        "tp": tp,
        "gold": ng,
        "pred": np_,
        "precision": tp / np_ if np_ else 0,
        "recall": tp / ng if ng else 0,
        "f1": 2 * tp / (ng + np_) if ng + np_ else 0,
    }


def normalize_b2(row):
    sent = row["sentence"]
    toks = row["tokens"]
    tags = row["list_of_selection_bio4"]
    assert list(sent) == toks
    assert len(tags) == len(toks)
    assert all(t in LSKT_LABELS for t in tags)
    return {"id": str(row["id"]).strip(), "tokens": toks, "tags": tags, "sentence": sent}


def main():
    a = arguments()
    import torch, numpy as np, transformers
    from transformers import AutoTokenizer, AutoModelForTokenClassification, DataCollatorForTokenClassification, get_linear_schedule_with_warmup

    assert len(a.revision) == 40
    train_rows = [normalize_b2(r) for r in read_jsonl(a.train)]
    dev_rows = [normalize_b2(r) for r in read_jsonl(a.dev)]
    gold_raw = read_jsonl(a.gold150)
    assert sha256(a.gold150) == FREEZE_SHA256
    gold_ids = {str(r.get("source_id") or r.get("id")).strip() for r in gold_raw}
    if a.smoke:
        train_rows = train_rows[:16]
        dev_rows = dev_rows[:16]
        a.epochs = 1
    else:
        assert len(train_rows) == 2150 and len(dev_rows) == 169
    # Gold150 never enters the training loader. Overlapping IDs (if any) stay eval-only.
    overlap = [r["id"] for r in train_rows + dev_rows if r["id"] in gold_ids]
    labels = list(LSKT_LABELS)
    ids = {t: i for i, t in enumerate(labels)}
    a.output.mkdir(parents=True, exist_ok=True)
    assert not (a.output / "config.json").exists(), "Use a new output directory"
    random.seed(a.seed)
    np.random.seed(a.seed)
    torch.manual_seed(a.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(a.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    assert device.type == "cuda"
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    tokenizer = AutoTokenizer.from_pretrained(a.model, revision=a.revision, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(
        a.model, revision=a.revision, num_labels=len(labels), id2label=dict(enumerate(labels)), label2id=ids
    ).to(device)
    limit = min(512, int(getattr(model.config, "max_position_embeddings", 512)) - 2)

    def encode_split(records):
        pieces, meta = [], []
        for row, r in enumerate(records):
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
                assert set(first) == set(range(stop - start)), "Tokenizer discarded a source character"
                encoded["labels"] = [-100] * len(encoded["input_ids"])
                for w, pos in first.items():
                    encoded["labels"][pos] = ids[r["tags"][start + w]]
                pieces.append(dict(encoded))
                meta.append((row, start, stop, first))
                start = stop
        return pieces, meta

    rows = {"train": train_rows, "dev": dev_rows}
    encoded = {s: encode_split(rs) for s, rs in rows.items()}
    collator = DataCollatorForTokenClassification(tokenizer)

    def loader(items, shuffle=False):
        return torch.utils.data.DataLoader(
            items, batch_size=a.batch_size, shuffle=shuffle, collate_fn=collator, generator=torch.Generator().manual_seed(a.seed)
        )

    def evaluate(split):
        model.eval()
        pred = [["O"] * len(r["tokens"]) for r in rows[split]]
        cursor = 0
        with torch.no_grad():
            for batch in loader(encoded[split][0]):
                outputs = model(**{k: v.to(device) for k, v in batch.items() if k != "labels"}).logits.argmax(-1).cpu().tolist()
                for output in outputs:
                    row, start, stop, first = encoded[split][1][cursor]
                    cursor += 1
                    for w, pos in first.items():
                        pred[row][start + w] = labels[output[pos]]
        assert cursor == len(encoded[split][1])
        metrics = span_f1([entities(r["tags"]) for r in rows[split]], [entities(p) for p in pred])
        return metrics, pred

    config = {
        **{k: (str(v) if isinstance(v, Path) else v) for k, v in vars(a).items()},
        "method": "chinese_lskt_linear_head_char_BIO_first_subword",
        "claim": "new LSKT head from fill-mask encoder; not JobBERT-zh CRF; not English-head map",
        "labels": labels,
        "chunk_word_limit": 128,
        "selection": "highest dev typed exact micro-F1; earliest epoch wins ties",
        "gold150_in_gradient": False,
        "gold150_in_selection": False,
        "gold150_id_overlap_in_used_splits": overlap,
        "train_sha256": sha256(a.train),
        "dev_sha256": sha256(a.dev),
        "gold150_sha256": sha256(a.gold150),
        "split_counts": {s: len(v) for s, v in rows.items()},
        "chunk_counts": {s: len(v[0]) for s, v in encoded.items()},
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "gpu": torch.cuda.get_device_name(0),
        "cuda": torch.version.cuda,
        "started_unix": time.time(),
    }
    (a.output / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    train_loader = loader(encoded["train"][0], shuffle=True)
    steps = len(train_loader) * a.epochs
    optimizer = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=0.01)
    scheduler = get_linear_schedule_with_warmup(optimizer, int(0.1 * steps), steps)
    best = -1
    best_epoch = None
    history = []
    for epoch in range(1, a.epochs + 1):
        model.train()
        losses = []
        for batch in train_loader:
            optimizer.zero_grad()
            loss = model(**{k: v.to(device) for k, v in batch.items()}).loss
            assert torch.isfinite(loss)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            losses.append(loss.item())
        metrics, _ = evaluate("dev")
        history.append({"epoch": epoch, "train_loss": float(np.mean(losses)), "dev": metrics})
        print(json.dumps(history[-1]), flush=True)
        if metrics["f1"] > best:
            best = metrics["f1"]
            best_epoch = epoch
            model.save_pretrained(a.output / "best")
            tokenizer.save_pretrained(a.output / "best")
        (a.output / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    del model
    torch.cuda.empty_cache()
    model = AutoModelForTokenClassification.from_pretrained(a.output / "best").to(device)
    result = {"status": "smoke_only" if a.smoke else "completed", "best_epoch": best_epoch, "dev_selection_f1": best}
    metrics, pred = evaluate("dev")
    result["dev"] = metrics
    with (a.output / "dev_predictions.jsonl").open("w", encoding="utf-8") as f:
        for i, tags in enumerate(pred):
            f.write(json.dumps({"id": rows["dev"][i]["id"], "list_of_selection_bio4": tags, "tokens": rows["dev"][i]["tokens"]}, ensure_ascii=False) + "\n")
    if not a.smoke:
        gold_bio = [convert_record(r) for r in gold_raw]
        gold_eval_rows = [{"id": r["id"], "tokens": r["tokens"], "tags": ["O"] * len(r["tokens"]), "sentence": r["sentence"]} for r in gold_bio]
        rows["gold150"] = gold_eval_rows
        encoded["gold150"] = encode_split(gold_eval_rows)
        _, gpred = evaluate("gold150")
        pred_path = a.output / "gold150_predictions.jsonl"
        with pred_path.open("w", encoding="utf-8") as f:
            for i, tags in enumerate(gpred):
                f.write(json.dumps({"id": gold_bio[i]["id"], "list_of_selection_bio4": tags, "tokens": gold_bio[i]["tokens"]}, ensure_ascii=False) + "\n")
        gold_bio_path = a.output / "gold150_gold.bio.jsonl"
        with gold_bio_path.open("w", encoding="utf-8") as f:
            for r in gold_bio:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        official = official_score(str(gold_bio_path), str(pred_path), align_mode="official", n_boot=2000, boot_seed=20260921)
        result["gold150_official"] = {
            "typed_exact_f1": official.get("typed_exact", official).get("f1") if isinstance(official.get("typed_exact", {}), dict) else None,
            "raw_keys": sorted(official.keys()),
        }
        (a.output / "gold150_official.json").write_text(json.dumps(official, indent=2, default=str), encoding="utf-8")
    (a.output / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in result if k != "gold150_official"}, default=str), flush=True)


if __name__ == "__main__":
    main()

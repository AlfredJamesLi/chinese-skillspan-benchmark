#!/usr/bin/env python3
"""Chinese RoBERTa-wwm-ext / JobBERT-zh + CRF token classifier.

Joint (default): 9 BIO tags. STL (`--keep_type L|K|S|T`): 3-tag CRF, other
types mapped to O. Trainer `--gold` is a side diagnostic (Gold v2). Paper-main
scoring is jieba + `scripts/eval_hybrid_cws_simhuman.py` on the V4 hybrid.
Does not overwrite frozen dumps, Gold v2, or hybrid gold.

Install: pip install -r requirements-train.txt
Default encoder: Hugging Face `AlfredJames/jobbert-zh`.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchcrf import CRF
from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup

from cnss_paths import paper_root  # noqa: E402

PAPER = paper_root()
sys.path.insert(0, str(PAPER / "scorer"))
from score_lskt import GOLD_FIELDS, extract_spans, match_exact, score  # noqa: E402

JOINT_LABELS = ["O", "B-L", "I-L", "B-K", "I-K", "B-S", "I-S", "B-T", "I-T"]
KEEP_TYPES = ("L", "K", "S", "T")


def label_maps(keep_type: str | None) -> tuple[list[str], dict[str, int], dict[int, str]]:
    """Joint = 9 BIO tags. STL = O/B-X/I-X for one type (unused types never trained)."""
    t = (keep_type or "").strip().upper()
    labels = ["O", f"B-{t}", f"I-{t}"] if t in KEEP_TYPES else list(JOINT_LABELS)
    l2i = {l: i for i, l in enumerate(labels)}
    return labels, l2i, {i: l for l, i in l2i.items()}


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_split(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith("["):
        return json.loads(raw)
    return [json.loads(l) for l in raw.splitlines() if l.strip()]


def cap_rows(rows: list[dict], n: int) -> list[dict]:
    return rows if n is None or n <= 0 else rows[:n]


def resolve_crf_pt(model_dir: str, init_crf: str, local_files_only: bool) -> Path | None:
    flag = (init_crf or "").strip()
    if not flag:
        return None
    if flag.lower() == "hub":
        from huggingface_hub import hf_hub_download

        return Path(hf_hub_download(model_dir, filename="crf/best.pt", local_files_only=local_files_only))
    p = Path(flag).expanduser()
    if not p.is_file():
        raise SystemExit(f"--init_crf file not found: {p}")
    return p


def gold_tags(rec: dict, keep_type: str | None = None) -> list[str]:
    tags = rec.get("list_of_selection_bio4") or rec.get("list_of_selection") or []
    out = []
    for t in tags:
        t = ("" if t is None else str(t)).strip() or "O"
        u = t.upper()
        if u in JOINT_LABELS:
            lab = u
        elif u in {"B", "I"}:
            lab = f"{u}-S"
        elif u.startswith("B-") or u.startswith("I-"):
            typ = u.split("-", 1)[1]
            lab = u if typ in KEEP_TYPES else f"{u[0]}-S"
        else:
            lab = "O"
        out.append(lab)
    kt = (keep_type or "").strip().upper()
    if kt in KEEP_TYPES:
        keep = {f"B-{kt}", f"I-{kt}"}
        out = [x if x in keep else "O" for x in out]
    return out


class SentDS(Dataset):
    def __init__(self, rows: list[dict], tokenizer, max_len: int, label2id: dict[str, int], keep_type: str | None = None):
        self.rows = rows
        self.tok = tokenizer
        self.max_len = max_len
        self.label2id = label2id
        self.keep_type = keep_type

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, i: int) -> dict:
        rec = self.rows[i]
        tokens = [str(t) for t in (rec.get("tokens") or list(rec.get("sentence") or ""))]
        tags = gold_tags(rec, self.keep_type)
        if len(tags) < len(tokens):
            tags = tags + ["O"] * (len(tokens) - len(tags))
        tags = tags[: len(tokens)]
        enc = self.tok(
            tokens,
            is_split_into_words=True,
            truncation=True,
            max_length=self.max_len,
            padding="max_length",
            return_tensors="pt",
        )
        word_ids = enc.word_ids(batch_index=0)
        lab = []
        prev = None
        for wid in word_ids:
            if wid is None or wid == prev:
                lab.append(0)
            else:
                lab.append(self.label2id.get(tags[wid], 0))
            prev = wid
        item = {k: v.squeeze(0) for k, v in enc.items()}
        # pytorch-crf requires mask[:, 0] all True. CLS is always position 0,
        # so use the tokenizer attention mask (CLS/SEP/subwords included, pads off).
        item["labels"] = torch.tensor(lab, dtype=torch.long)
        item["crf_mask"] = item["attention_mask"].bool()
        item["word_ids"] = torch.tensor(
            [-1 if w is None else int(w) for w in word_ids], dtype=torch.long
        )
        item["n_words"] = len(tokens)
        item["idx"] = i
        return item


class BertCRF(nn.Module):
    def __init__(self, model_dir: str, n_labels: int, dropout: float = 0.1, local_files_only: bool = False):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(model_dir, local_files_only=local_files_only)
        h = self.encoder.config.hidden_size
        self.dropout = nn.Dropout(dropout)
        self.emissions = nn.Linear(h, n_labels)
        self.crf = CRF(n_labels, batch_first=True)

    def forward(self, input_ids, attention_mask, token_type_ids=None, labels=None, crf_mask=None):
        kwargs = {"input_ids": input_ids, "attention_mask": attention_mask}
        if token_type_ids is not None:
            kwargs["token_type_ids"] = token_type_ids
        hidden = self.encoder(**kwargs).last_hidden_state
        em = self.emissions(self.dropout(hidden))
        mask = crf_mask if crf_mask is not None else attention_mask.bool()
        if not mask[:, 0].all():
            mask = mask.clone()
            mask[:, 0] = True
        loss = None
        if labels is not None:
            loss = -self.crf(em, labels, mask=mask, reduction="mean")
        return em, mask, loss

    def decode(self, emissions, mask) -> list[list[int]]:
        return self.crf.decode(emissions, mask=mask)


def apply_decode(word_ids, decoded: list[int], n_words: int, id2label: dict[int, str]) -> list[str]:
    """Map CRF tags (one per non-pad tokenizer position, incl. CLS/SEP) onto words.

    First subword keeps its tag; CLS/SEP and continuation subwords are ignored.
    """
    out = ["O"] * n_words
    prev = None
    n = min(len(word_ids), len(decoded))
    for i in range(n):
        wid = word_ids[i]
        if wid is None or wid == prev:
            if wid is not None:
                prev = wid
            continue
        if wid < n_words:
            out[wid] = id2label.get(decoded[i], "O")
        prev = wid
    return out


@torch.no_grad()
def predict_tags(model, tokenizer, rows, max_len, device, bsz: int, label2id, id2label, keep_type: str | None) -> list[list[str]]:
    model.eval()
    ds = SentDS(rows, tokenizer, max_len, label2id, keep_type)
    loader = DataLoader(ds, batch_size=bsz, shuffle=False)
    all_tags: list[list[str] | None] = [None] * len(rows)
    for batch in loader:
        idxs = batch.pop("idx").tolist()
        n_words = batch.pop("n_words").tolist()
        word_ids = batch.pop("word_ids")
        crf_mask = batch.pop("crf_mask").to(device)
        batch.pop("labels")
        batch = {k: v.to(device) for k, v in batch.items()}
        em, mask, _ = model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            token_type_ids=batch.get("token_type_ids"),
            crf_mask=crf_mask,
        )
        decoded = model.decode(em, mask)
        for i, idx in enumerate(idxs):
            wids = [None if int(w) < 0 else int(w) for w in word_ids[i].tolist()]
            all_tags[idx] = apply_decode(wids, decoded[i], int(n_words[i]), id2label)
    return [t or ["O"] * len(r.get("tokens") or []) for t, r in zip(all_tags, rows)]


def typed_f1(rows: list[dict], pred_tags: list[list[str]], keep_type: str | None = None) -> float:
    tp = fp = fn = 0
    for rec, pt in zip(rows, pred_tags):
        gold = gold_tags(rec, keep_type)
        n = len(rec.get("tokens") or gold)
        gold = (gold + ["O"] * n)[:n]
        pt = (pt + ["O"] * n)[:n]
        rec_g = {"tokens": ["x"] * n, "list_of_selection_bio4": gold}
        rec_p = {"tokens": ["x"] * n, "list_of_selection_bio4": pt}
        m = match_exact(extract_spans(rec_g, GOLD_FIELDS), extract_spans(rec_p, GOLD_FIELDS))
        tp += m["tp"]
        fp += m["fp"]
        fn += m["fn"]
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def write_pred_jsonl(rows: list[dict], pred_tags: list[list[str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec, pt in zip(rows, pred_tags):
            out = {
                "id": rec.get("id"),
                "global_id": rec.get("global_id"),
                "sentence": rec.get("sentence"),
                "tokens": rec.get("tokens"),
                "pred_tags": pt,
                "list_of_selection_bio4": pt,
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")


def train_one(args) -> dict:
    set_seed(args.seed)
    keep_type = (args.keep_type or "").strip().upper() or None
    if keep_type and keep_type not in KEEP_TYPES:
        raise ValueError(f"keep_type must be one of {KEEP_TYPES} or empty, got {args.keep_type!r}")
    _, label2id, id2label = label_maps(keep_type)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(args.model_dir, local_files_only=args.local_files_only)
    model = BertCRF(
        args.model_dir, n_labels=len(label2id), local_files_only=args.local_files_only
    ).to(device)
    crf_pt = resolve_crf_pt(args.model_dir, getattr(args, "init_crf", "") or "", args.local_files_only)
    if crf_pt is not None:
        state = torch.load(crf_pt, map_location="cpu")
        model.load_state_dict(state)
        print(json.dumps({"init_crf": str(crf_pt)}), flush=True)
    train_rows = cap_rows(load_split(Path(args.train)), int(getattr(args, "max_train", 0) or 0))
    dev_rows = cap_rows(load_split(Path(args.dev)), int(getattr(args, "max_dev", 0) or 0))
    test_rows = cap_rows(load_split(Path(args.test)), int(getattr(args, "max_test", 0) or 0))
    if bool(getattr(args, "predict_only", False)):
        train_rows = []
    print(json.dumps({"n_train": len(train_rows), "n_dev": len(dev_rows), "n_test": len(test_rows)}), flush=True)
    train_ds = SentDS(train_rows, tok, args.max_len, label2id, keep_type)
    loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    total = max(1, len(loader) * args.epochs)
    sched = get_linear_schedule_with_warmup(opt, int(0.1 * total), total)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = out_dir / "last.ckpt"
    start_epoch, best_f1, patience, history = 1, -1.0, 0, []
    if args.resume and ckpt_path.is_file():
        ckpt = torch.load(ckpt_path, map_location="cpu")
        model.load_state_dict(ckpt["model"])
        opt.load_state_dict(ckpt["opt"])
        sched.load_state_dict(ckpt["sched"])
        start_epoch = int(ckpt["epoch"]) + 1
        best_f1 = float(ckpt.get("best_f1", -1.0))
        patience = int(ckpt.get("patience", 0))
        history = list(ckpt.get("history") or [])
        print(json.dumps({"resume_from": str(ckpt_path), "next_epoch": start_epoch, "best_f1": best_f1}), flush=True)
    predict_only = bool(getattr(args, "predict_only", False))
    if predict_only:
        print(json.dumps({"predict_only": True}), flush=True)
    for epoch in range(start_epoch, args.epochs + 1):
        if predict_only:
            break
        model.train()
        losses = []
        for step, batch in enumerate(loader, start=1):
            batch.pop("idx")
            batch.pop("word_ids")
            batch.pop("n_words")
            crf_mask = batch.pop("crf_mask").to(device)
            labels = batch.pop("labels").to(device)
            batch = {k: v.to(device) for k, v in batch.items()}
            _, _, loss = model(
                input_ids=batch["input_ids"],
                attention_mask=batch["attention_mask"],
                token_type_ids=batch.get("token_type_ids"),
                labels=labels,
                crf_mask=crf_mask,
            )
            opt.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            losses.append(float(loss.item()))
            if step % 200 == 0:
                print(json.dumps({"epoch": epoch, "step": step, "loss": float(loss.item())}), flush=True)
        dev_pred = predict_tags(
            model, tok, dev_rows, args.max_len, device, args.batch_size, label2id, id2label, keep_type
        )
        if device.type == "cuda":
            torch.cuda.empty_cache()
        dev_f1 = typed_f1(dev_rows, dev_pred, keep_type)
        row = {"epoch": epoch, "train_loss": sum(losses) / len(losses), "dev_typed_f1": dev_f1}
        history.append(row)
        print(json.dumps(row), flush=True)
        if dev_f1 > best_f1 + 1e-4:
            best_f1 = dev_f1
            patience = 0
            torch.save(model.state_dict(), out_dir / "best.pt")
        else:
            patience += 1
        if not bool(getattr(args, "smoke", False)):
            torch.save(
                {
                    "model": model.state_dict(),
                    "opt": opt.state_dict(),
                    "sched": sched.state_dict(),
                    "epoch": epoch,
                    "best_f1": best_f1,
                    "patience": patience,
                    "history": history,
                },
                ckpt_path,
            )
        if patience >= args.patience:
            print(f"early stop at epoch {epoch}", flush=True)
            break
    best_path = out_dir / "best.pt"
    if best_path.is_file():
        model.load_state_dict(torch.load(best_path, map_location=device))
    test_pred = predict_tags(
        model, tok, test_rows, args.max_len, device, args.batch_size, label2id, id2label, keep_type
    )
    pred_path = out_dir / "test_pred.jsonl"
    write_pred_jsonl(test_rows, test_pred, pred_path)
    skip_score = bool(getattr(args, "skip_score", False))
    report: dict = {}
    if not skip_score:
        report = score(
            args.gold,
            str(pred_path),
            align_mode="official",
            pred_fields=("pred_tags", "list_of_selection_bio4"),
            n_boot=0,
        )
        (out_dir / "score_official.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    (out_dir / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    meta = {
        "seed": args.seed,
        "model_dir": args.model_dir,
        "keep_type": keep_type,
        "n_labels": len(label2id),
        "best_dev_typed_f1": best_f1,
        "history": history,
        "pred_path": str(pred_path),
        "alignment_ok": report.get("alignment_ok"),
        "typed_exact": report.get("typed_exact"),
        "collapsed_exact": report.get("collapsed_exact"),
        "gold_sha256": report.get("gold_sha256"),
        "pred_sha256": report.get("pred_sha256"),
        "scorer_version": report.get("scorer_version"),
    }
    (out_dir / "run_summary.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"seed": args.seed, "keep_type": keep_type, "best_dev": best_f1, "test_typed": (report.get("typed_exact") or {}).get("f1"), "test_collapsed": (report.get("collapsed_exact") or {}).get("f1"), "align": report.get("alignment_ok")}, ensure_ascii=False), flush=True)
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", default="AlfredJames/jobbert-zh")
    ap.add_argument("--train", default=str(PAPER / "data/train_lskt_v4_silver.jsonl"))
    ap.add_argument("--dev", default=str(PAPER / "data/dev_lskt_v4_silver.jsonl"))
    ap.add_argument("--test", default=str(PAPER / "data/corpus_splits/test.json"))
    ap.add_argument("--gold", default=str(PAPER / "data/gold_canonical_v2.jsonl"))
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--patience", type=int, default=2)
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--max_len", type=int, default=256)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument(
        "--local_files_only",
        action="store_true",
        help="Do not download from the Hub (laboratory cache / offline).",
    )
    ap.add_argument(
        "--keep_type",
        default="",
        help="STL: keep only L, K, S, or T (other BIO → O; 3-tag CRF). Empty = joint 9-tag LSKT.",
    )
    ap.add_argument("--max_train", type=int, default=0, help="Cap train rows (0 = all).")
    ap.add_argument("--max_dev", type=int, default=0, help="Cap dev rows (0 = all).")
    ap.add_argument("--max_test", type=int, default=0, help="Cap test rows (0 = all).")
    ap.add_argument(
        "--init_crf",
        default="",
        help="Load a BertCRF state_dict. Path, or 'hub' for <model_dir>/crf/best.pt.",
    )
    ap.add_argument("--predict_only", action="store_true", help="Skip the training loop; write test_pred.jsonl.")
    ap.add_argument("--skip_score", action="store_true", help="Do not call the official scorer (smoke / partial test).")
    ap.add_argument(
        "--smoke",
        action="store_true",
        help="Hub connectivity check: 16/8/8 rows, 1 epoch, skip scorer. Not a paper F1.",
    )
    args = ap.parse_args()
    if args.smoke:
        args.max_train = args.max_train or 16
        args.max_dev = args.max_dev or 8
        args.max_test = args.max_test or 8
        args.epochs = 1
        args.patience = 1
        args.batch_size = min(int(args.batch_size), 4)
        args.skip_score = True
    if args.predict_only and not (args.init_crf or args.resume):
        raise SystemExit("--predict_only needs --init_crf or --resume")
    train_one(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

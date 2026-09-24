#!/usr/bin/env python3
"""Finish remaining Chinese + native SkillSpan + Gnehm ICT cells on 2 GPUs.

Skips any cell that already has result.json. Retries failed cells.
Does not touch completed common-protocol 48-cell directories.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/home/guojingli3/cnss_external_benchmarks_20260921")
SS = ROOT / "upstream_full" / "SkillSpan"
PY = ROOT / "env" / "bin" / "python"
LOGDIR = ROOT / "logs"
MACHAMP_TRAIN = SS / "machamp" / "train.py"
MACHAMP_PREDICT = SS / "machamp" / "predict.py"

SKILLSPAN_MODELS = ["jobbert", "jobspanbert", "bert", "spanbert"]
SKILLSPAN_TASKS = ["skills", "knowledge"]  # skip multi for today's wall clock
SKILLSPAN_SEEDS = [3477689, 4213916, 8749520, 6828303, 9364029]
GNEHM_SEEDS = [276800, 381552, 497646, 624189, 884832]


def env_for_gpu(gpu: str) -> dict:
    e = os.environ.copy()
    e["CUDA_VISIBLE_DEVICES"] = str(gpu)
    e["HF_HOME"] = str(ROOT / "hf_cache")
    e["HF_HUB_CACHE"] = str(ROOT / "hf_cache" / "hub")
    e["TRANSFORMERS_CACHE"] = str(ROOT / "hf_cache" / "hub")
    e["TOKENIZERS_PARALLELISM"] = "false"
    e["PYTHONNOUSERSITE"] = "1"
    return e


def bio_spans(tags):
    out = set()
    start = None
    kind = None
    for i, t in enumerate(list(tags) + ["O"]):
        t = t or "O"
        if t in ("O", "X", "_"):
            prefix, typ = "O", ""
        else:
            parts = t.split("-", 1)
            prefix = parts[0]
            typ = parts[1] if len(parts) > 1 else "SPAN"
        if start is not None and (prefix not in ("I", "E") or typ != kind):
            out.add((start, i, kind))
            start = None
        if prefix in ("B", "S") or (prefix in ("I", "E") and start is None):
            start = i
            kind = typ
        if prefix in ("S", "E") and start is not None:
            out.add((start, i + 1, kind))
            start = None
    return out


def read_conll_sents(path: Path, tag_col: int):
    sents = []
    toks, tags = [], []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            if toks:
                sents.append((toks, tags))
                toks, tags = [], []
            continue
        parts = raw.split("\t") if "\t" in raw else raw.split()
        toks.append(parts[0])
        tags.append(parts[tag_col] if len(parts) > tag_col else "O")
    if toks:
        sents.append((toks, tags))
    return sents


def score_aligned(gold_sents, pred_sents):
    n = min(len(gold_sents), len(pred_sents))
    gold = [bio_spans(gold_sents[i][1]) for i in range(n)]
    pred = [bio_spans(pred_sents[i][1]) for i in range(n)]
    tp = sum(len(g & p) for g, p in zip(gold, pred))
    ng = sum(map(len, gold))
    np_ = sum(map(len, pred))
    return {
        "n_sents": n,
        "gold_n_sents": len(gold_sents),
        "pred_n_sents": len(pred_sents),
        "tp": tp,
        "gold": ng,
        "pred": np_,
        "precision": tp / np_ if np_ else 0.0,
        "recall": tp / ng if ng else 0.0,
        "f1": (2 * tp / (ng + np_)) if (ng + np_) else 0.0,
    }


def wait_pool(procs: dict, n_workers: int):
    while len(procs) >= n_workers:
        time.sleep(10)
        for pid, rec in list(procs.items()):
            rc = rec["proc"].poll()
            if rc is None:
                continue
            rec["log"].close()
            print(f"[end] gpu={rec['gpu']} {rec['name']} rc={rc}", flush=True)
            rec["rc"] = rc
            procs.pop(pid)
            return rec
    return None


def drain(procs: dict):
    results = []
    while procs:
        rec = wait_pool(procs, 1)
        if rec:
            results.append(rec)
    return results


def latest_model_pt(name: str) -> Path | None:
    base = SS / "logs" / name
    if not base.exists():
        return None
    pts = sorted(base.glob("*/model.pt"), key=lambda p: p.stat().st_mtime)
    return pts[-1] if pts else None


def latest_metrics(name: str):
    base = SS / "logs" / name
    mets = sorted(base.glob("*/metrics.json"), key=lambda p: p.stat().st_mtime)
    if not mets:
        return None, None
    return mets[-1], json.loads(mets[-1].read_text())


def run_cmd(cmd, env, log_path: Path, cwd: Path, timeout=None) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as lf:
        lf.write(f"\n# CMD {' '.join(str(x) for x in cmd)}\n")
        lf.flush()
        p = subprocess.run(cmd, env=env, cwd=str(cwd), stdout=lf, stderr=subprocess.STDOUT, timeout=timeout)
    return p.returncode


def chinese_cells():
    pins = {r["model"]: r["revision"] for r in json.loads((ROOT / "models.json").read_text())}
    cells = []
    mapping = {
        "xlm-roberta-large": "FacebookAI/xlm-roberta-large",
        "esco-xlm-roberta-large": "jjzha/esco-xlm-roberta-large",
    }
    for short, model in mapping.items():
        for seed in (42, 43, 44):
            out = ROOT / "runs" / "chinese" / "full" / short / str(seed)
            if (out / "result.json").exists():
                continue
            cells.append((short, model, pins[model], seed, out))
    return cells


def run_chinese_one(short, model, rev, seed, out: Path, gpu: str, attempt: int) -> int:
    if out.exists() and not (out / "result.json").exists():
        shutil.rmtree(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    log = LOGDIR / f"chinese_full_{short}_{seed}_try{attempt}.out"
    cmd = [
        str(PY),
        str(ROOT / "run_chinese_encoder.py"),
        "--model",
        model,
        "--revision",
        rev,
        "--seed",
        str(seed),
        "--output",
        str(out),
    ]
    print(f"[chinese start] gpu={gpu} {short} seed={seed} try={attempt}", flush=True)
    rc = run_cmd(cmd, env_for_gpu(gpu), log, ROOT)
    print(f"[chinese end] gpu={gpu} {short} seed={seed} rc={rc}", flush=True)
    return rc


def skillspan_cells():
    cells = []
    for model in SKILLSPAN_MODELS:
        for task in SKILLSPAN_TASKS:
            for seed in SKILLSPAN_SEEDS:
                out = ROOT / "runs" / "native" / "skillspan" / model / task / str(seed)
                if (out / "result.json").exists():
                    continue
                cells.append((model, task, seed, out))
    return cells


def score_skillspan_test(model: str, task: str, seed: int, out: Path, env: dict) -> dict:
    name = f"skill.{model}.{task}.{seed}"
    pt = latest_model_pt(name)
    if pt is None:
        raise FileNotFoundError(f"no model.pt for {name}")
    pred_dir = out / "preds"
    pred_dir.mkdir(parents=True, exist_ok=True)
    site_scores = {}
    gold_col = 1 if task == "skills" else 2
    for site in ("house", "tech"):
        gold = SS / "data" / "conll" / f"skillspan_{site}_test.conll"
        pred = pred_dir / f"{task}.{site}.test.{seed}.out"
        ds = site
        rc = run_cmd(
            [str(PY), str(MACHAMP_PREDICT), str(pt), str(gold), str(pred), "--dataset", ds, "--device", "0"],
            env,
            LOGDIR / f"native_ss_predict_{model}_{task}_{seed}_{site}.out",
            SS,
        )
        if rc != 0:
            raise RuntimeError(f"predict {site} rc={rc}")
        gold_sents = read_conll_sents(gold, gold_col)
        # MaChAmp keeps original CoNLL columns; the task tag is the same column as gold.
        pred_sents_raw = read_conll_sents(pred, gold_col)
        site_scores[site] = score_aligned(gold_sents, pred_sents_raw)
    # pooled
    gold_all, pred_all = [], []
    for site in ("house", "tech"):
        gold = SS / "data" / "conll" / f"skillspan_{site}_test.conll"
        pred = pred_dir / f"{task}.{site}.test.{seed}.out"
        gold_all.extend(read_conll_sents(gold, gold_col))
        pred_all.extend(read_conll_sents(pred, gold_col))
    pooled = score_aligned(gold_all, pred_all)
    met_path, metrics = latest_metrics(name)
    return {"house": site_scores["house"], "tech": site_scores["tech"], "pooled": pooled, "dev_metrics_file": str(met_path) if met_path else None, "dev_metrics": metrics, "model_pt": str(pt)}


def run_skillspan_one(model: str, task: str, seed: int, out: Path, gpu: str, attempt: int) -> int:
    name = f"skill.{model}.{task}.{seed}"
    logdir = SS / "logs" / name
    if logdir.exists() and not (out / "result.json").exists():
        shutil.rmtree(logdir)
    out.mkdir(parents=True, exist_ok=True)
    env = env_for_gpu(gpu)
    train_log = LOGDIR / f"native_ss_train_{model}_{task}_{seed}_try{attempt}.out"
    cmd = [
        str(PY),
        str(MACHAMP_TRAIN),
        "--dataset_configs",
        str(SS / "configs" / f"{task}.json"),
        "--parameters_config",
        str(SS / "configs" / f"{model}.json"),
        "--name",
        name,
        "--seed",
        str(seed),
        "--device",
        "0",
    ]
    print(f"[ss start] gpu={gpu} {name} try={attempt}", flush=True)
    rc = run_cmd(cmd, env, train_log, SS)
    if rc != 0:
        print(f"[ss train fail] {name} rc={rc}", flush=True)
        return rc
    try:
        scored = score_skillspan_test(model, task, seed, out, env)
    except Exception as e:
        (out / "error.txt").write_text(str(e))
        print(f"[ss score fail] {name} {e}", flush=True)
        return 2
    best_epoch = None
    dev_f1 = None
    if scored.get("dev_metrics"):
        best_epoch = scored["dev_metrics"].get("best_epoch")
        for k, v in scored["dev_metrics"].items():
            if k.startswith("best_dev_") and k.endswith("_span_f1"):
                dev_f1 = v
    result = {
        "status": "completed",
        "track": "native",
        "dataset": "skillspan",
        "subset": "public_house_tech",
        "model": model,
        "task": task,
        "seed": seed,
        "best_epoch": best_epoch,
        "dev_span_f1": dev_f1,
        "test": scored["pooled"],
        "test_house": scored["house"],
        "test_tech": scored["tech"],
        "model_pt": scored["model_pt"],
        "protocol_id": "native_skillspan_machamp_20ep_20260922",
        "notes": "MaChAmp seq_bio CRF; public HOUSE+TECH only; not BIG; not common linear-head protocol.",
    }
    (out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"[ss end] {name} pooled_f1={scored['pooled']['f1']:.4f}", flush=True)
    return 0


def ensure_gnehm_jobbert_de_config() -> Path:
    src = (SS / "configs" / "jobbert.json").read_text()
    dst = ROOT / "patches" / "gnehm_native" / "jobbert-de.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.replace("jjzha/jobbert-base-cased", "agne/jobBERT-de"))
    return dst


def gnehm_cells():
    cells = []
    spec = [
        ("jobbert-de", str(ensure_gnehm_jobbert_de_config()), "native_gnehm_jobbert_de_machamp_20ep_20260922"),
        ("escoxlmr", str(ROOT / "patches" / "escoxlmr_configs" / "gnehm" / "escoxlmr.json"), "native_gnehm_escoxlmr_machamp_5ep_20260922"),
    ]
    for model, cfg, protocol in spec:
        for seed in GNEHM_SEEDS:
            out = ROOT / "runs" / "native" / "gnehm_ict" / model / str(seed)
            if (out / "result.json").exists():
                continue
            cells.append((model, cfg, protocol, seed, out))
    return cells


def run_gnehm_one(model: str, cfg: str, protocol: str, seed: int, out: Path, gpu: str, attempt: int) -> int:
    name = f"gnehm.{model}.ict.{seed}"
    logdir = SS / "logs" / name
    if logdir.exists() and not (out / "result.json").exists():
        shutil.rmtree(logdir)
    out.mkdir(parents=True, exist_ok=True)
    env = env_for_gpu(gpu)
    train_log = LOGDIR / f"native_gnehm_train_{model}_{seed}_try{attempt}.out"
    ds_cfg = ROOT / "patches" / "gnehm_native" / "ict.json"
    cmd = [
        str(PY),
        str(MACHAMP_TRAIN),
        "--dataset_configs",
        str(ds_cfg),
        "--parameters_config",
        cfg,
        "--name",
        name,
        "--seed",
        str(seed),
        "--device",
        "0",
    ]
    print(f"[gnehm start] gpu={gpu} {name} try={attempt}", flush=True)
    rc = run_cmd(cmd, env, train_log, SS)
    if rc != 0:
        print(f"[gnehm train fail] {name} rc={rc}", flush=True)
        return rc
    pt = latest_model_pt(name)
    if pt is None:
        return 2
    gold = ROOT / "native_data" / "gnehm" / "test.conll"
    pred = out / "test.pred.conll"
    rc = run_cmd(
        [str(PY), str(MACHAMP_PREDICT), str(pt), str(gold), str(pred), "--dataset", "gnehm", "--device", "0"],
        env,
        LOGDIR / f"native_gnehm_predict_{model}_{seed}.out",
        SS,
    )
    if rc != 0:
        return rc
    scored = score_aligned(read_conll_sents(gold, 1), read_conll_sents(pred, -1))
    met_path, metrics = latest_metrics(name)
    best_epoch = metrics.get("best_epoch") if metrics else None
    dev_f1 = None
    if metrics:
        for k, v in metrics.items():
            if k.startswith("best_dev_") and k.endswith("_span_f1"):
                dev_f1 = v
    result = {
        "status": "completed",
        "track": "native",
        "dataset": "gnehm",
        "subset": "public_ict",
        "model": model,
        "task": "ict_span",
        "seed": seed,
        "best_epoch": best_epoch,
        "dev_span_f1": dev_f1,
        "test": scored,
        "model_pt": str(pt),
        "protocol_id": protocol,
        "notes": "Public ICT CoNLL only. Not Gnehm 2022 EDU/EXP/LNG. jobBERT-de uses SkillSpan MaChAmp 20-epoch template; ESCOXLM-R uses original 5-epoch Gnehm config.",
    }
    (out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"[gnehm end] {name} test_f1={scored['f1']:.4f}", flush=True)
    return 0


def run_phase(label, cells, runner, workers: int, retries: int):
    print(f"[{label}] {len(cells)} remaining cells", flush=True)
    if not cells:
        return []
    pending = [(cell, 1) for cell in cells]
    failed = []
    inflight = {}
    gpu_ids = ["0", "1"][:workers]

    def free_gpu():
        used = {rec["gpu"] for rec in inflight.values()}
        for g in gpu_ids:
            if g not in used:
                return g
        return None

    idx = 0
    while pending or inflight:
        while pending and free_gpu() is not None:
            cell, attempt = pending.pop(0)
            gpu = free_gpu()
            log = LOGDIR / f"{label}_worker.log"
            # Launch in a child process so two cells run concurrently.
            # Runner is blocking; wrap with multiprocessing via subprocess of this file is heavy.
            # Instead use a thread-like Popen of a tiny helper encoded as PYTHON one-shot.
            # Simpler: sequential pair wait implemented with subprocess.Popen of a dedicated argv.
            break
        # Use explicit pair scheduling below.
        break

    # Pairwise scheduling with subprocess.Popen of this script's one-cell mode.
    queue = [(cell, 1) for cell in cells]
    inflight = {}
    while queue or inflight:
        while queue and len(inflight) < workers:
            cell, attempt = queue.pop(0)
            used = {v["gpu"] for v in inflight.values()}
            gpu = next(g for g in gpu_ids if g not in used)
            helper = {
                "label": label,
                "cell": encode_cell(label, cell),
                "gpu": gpu,
                "attempt": attempt,
            }
            helper_path = LOGDIR / f"cell_{label}_{idx}_{attempt}.json"
            idx += 1
            helper_path.write_text(json.dumps(helper))
            logf = (LOGDIR / f"{label}_{idx}_{attempt}.wrapper.out").open("w")
            proc = subprocess.Popen(
                [str(PY), str(Path(__file__)), "--one-cell", str(helper_path)],
                env=env_for_gpu(gpu),
                stdout=logf,
                stderr=subprocess.STDOUT,
            )
            inflight[proc.pid] = {"proc": proc, "gpu": gpu, "name": helper["cell"], "log": logf, "cell": cell, "attempt": attempt, "helper": helper_path}
            print(f"[start] gpu={gpu} {label} {helper['cell']} try={attempt}", flush=True)
        time.sleep(8)
        for pid, rec in list(inflight.items()):
            rc = rec["proc"].poll()
            if rc is None:
                continue
            rec["log"].close()
            print(f"[end] gpu={rec['gpu']} {rec['name']} rc={rc}", flush=True)
            inflight.pop(pid)
            if rc != 0 and rec["attempt"] < retries:
                print(f"[retry] {rec['name']} next_try={rec['attempt']+1}", flush=True)
                queue.append((rec["cell"], rec["attempt"] + 1))
            elif rc != 0:
                failed.append((rec["name"], rc))
    return failed


def encode_cell(label, cell):
    if label == "chinese":
        short, model, rev, seed, out = cell
        return f"{short}/{seed}"
    if label == "skillspan":
        model, task, seed, out = cell
        return f"{model}/{task}/{seed}"
    model, cfg, protocol, seed, out = cell
    return f"{model}/{seed}"


def run_one_cell(helper_path: Path) -> int:
    h = json.loads(helper_path.read_text())
    label = h["label"]
    gpu = h["gpu"]
    attempt = h["attempt"]
    if label == "chinese":
        return run_chinese_from_name(h["cell"], gpu, attempt)
    if label == "skillspan":
        return run_skillspan_from_name(h["cell"], gpu, attempt)
    if label == "gnehm":
        return run_gnehm_from_name(h["cell"], gpu, attempt)
    return 3


def chinese_cells_all():
    pins = {r["model"]: r["revision"] for r in json.loads((ROOT / "models.json").read_text())}
    mapping = {
        "xlm-roberta-large": "FacebookAI/xlm-roberta-large",
        "esco-xlm-roberta-large": "jjzha/esco-xlm-roberta-large",
    }
    cells = []
    for short, model in mapping.items():
        for seed in (42, 43, 44):
            out = ROOT / "runs" / "chinese" / "full" / short / str(seed)
            cells.append((short, model, pins[model], seed, out))
    return cells


def run_chinese_from_name(name: str, gpu: str, attempt: int) -> int:
    short, seed_s = name.split("/")
    seed = int(seed_s)
    for c in chinese_cells_all():
        if c[0] == short and c[3] == seed:
            if (c[4] / "result.json").exists():
                return 0
            return run_chinese_one(*c, gpu, attempt)
    return 4


def run_skillspan_from_name(name: str, gpu: str, attempt: int) -> int:
    model, task, seed_s = name.split("/")
    seed = int(seed_s)
    out = ROOT / "runs" / "native" / "skillspan" / model / task / str(seed)
    if (out / "result.json").exists():
        return 0
    return run_skillspan_one(model, task, seed, out, gpu, attempt)


def run_gnehm_from_name(name: str, gpu: str, attempt: int) -> int:
    model, seed_s = name.split("/")
    seed = int(seed_s)
    if model == "jobbert-de":
        cfg = str(ensure_gnehm_jobbert_de_config())
        protocol = "native_gnehm_jobbert_de_machamp_20ep_20260922"
    else:
        cfg = str(ROOT / "patches" / "escoxlmr_configs" / "gnehm" / "escoxlmr.json")
        protocol = "native_gnehm_escoxlmr_machamp_5ep_20260922"
    out = ROOT / "runs" / "native" / "gnehm_ict" / model / str(seed)
    if (out / "result.json").exists():
        return 0
    return run_gnehm_one(model, cfg, protocol, seed, out, gpu, attempt)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workers", type=int, default=2)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--one-cell", type=Path, default=None)
    p.add_argument("--skip-chinese", action="store_true")
    p.add_argument("--skip-native", action="store_true")
    p.add_argument("--skip-gnehm", action="store_true")
    args = p.parse_args()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    if args.one_cell:
        sys.exit(run_one_cell(args.one_cell))

    print(f"[remaining_today] host start {time.strftime('%Y-%m-%dT%H:%M:%S')} workers={args.workers}", flush=True)
    failed = []
    if not args.skip_chinese:
        failed += run_phase("chinese", chinese_cells(), None, args.workers, args.retries)
    if not args.skip_native:
        failed += run_phase("skillspan", skillspan_cells(), None, args.workers, args.retries)
    if not args.skip_gnehm:
        failed += run_phase("gnehm", gnehm_cells(), None, args.workers, args.retries)
    print(json.dumps({"failed": failed}, indent=2), flush=True)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

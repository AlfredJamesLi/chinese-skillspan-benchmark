# 服务器 B 第三步：读出两臂 hybrid_eval 的 P/R / alignment

**能自己算：能。** 不占 GPU、不重训。`eval_one_hybrid_cws.py` 在 2d 结束时已把这些字段写进 `hybrid_eval.json`。本步只是读出来做成对照表；文件缺失时才用 CPU 重评一次。

不要写 abstract，不要改 Gold，不要开 3-seed / DAPT。

对照（已确认，只用来比形状，不要改这些数）：

| 系统 | P | R | exact F1 |
|---|---:|---:|---:|
| JobBERT 3M v4 + jieba | 0.4730 | 0.3994 | 0.4331 |
| JobBERT 1M v4 + jieba | 0.4685 | 0.3925 | 0.4272 |

---

## PROMPT（贴到服务器 B）

工作区仍是 `/home/guojingli3/Chinese-Skillspan-Benchmark`。软链不要改。不要用 GPU。不要重训 CRF。不要打 Table 3 / 2676。数字标 **待验证**。

任务：汇总两臂 `hybrid_eval.json` 里的 **alignment、n、P/R/F1、jieba 填充、短长跨度**。这些在 2d 里应该已经算过。

### 3a. 先找文件

```bash
WORK=/home/guojingli3/Chinese-Skillspan-Benchmark
PAPER="$WORK/Chinese_skill_benchmark_Paper"
ls -l \
  "$PAPER/output/vanilla_wwm_base_v4_silver_seed42/hybrid_eval.json" \
  "$PAPER/output/vanilla_wwm_base_v4_silver_seed42/test_pred.jsonl" \
  "$PAPER/output/vanilla_wwm_base_v4_silver_seed42/test_pred_cws.jsonl" \
  "$PAPER/output/vanilla_wwm_base_v4_silver_seed42/history.json" \
  "$PAPER/output/vanilla_wwm_large_v4_silver_seed42/hybrid_eval.json" \
  "$PAPER/output/vanilla_wwm_large_v4_silver_seed42/test_pred.jsonl" \
  "$PAPER/output/vanilla_wwm_large_v4_silver_seed42/test_pred_cws.jsonl" \
  "$PAPER/output/vanilla_wwm_large_v4_silver_seed42/history.json" \
  "$PAPER/output/vanilla_wwm_v4/compare_seed42.json"
```

### 3b. 若 `hybrid_eval.json` 已在：只读，不要重跑

用本机 `python3`（`/home/guojingli3/miniconda3/envs/adasparse/bin/python3`）执行下面脚本，打印一张表 + 一份 `pr_alignment_seed42.json`。

```bash
export SCESC_ROOT=/home/guojingli3/Chinese-Skillspan-Benchmark
export PYTHONPATH="$SCESC_ROOT/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
python3 - << 'PY'
import json
from pathlib import Path
PAPER = Path("/home/guojingli3/Chinese-Skillspan-Benchmark/Chinese_skill_benchmark_Paper")
arms = {
    "vanilla_wwm_base": PAPER / "output/vanilla_wwm_base_v4_silver_seed42",
    "vanilla_wwm_large": PAPER / "output/vanilla_wwm_large_v4_silver_seed42",
}
ref = {
    "JobBERT_3M_v4_confirmed": {"p": 0.4730, "r": 0.3994, "f1": 0.4331},
    "JobBERT_1M_v4_confirmed": {"p": 0.4685, "r": 0.3925, "f1": 0.4272},
}

def bands(rows):
    out = {}
    for row in rows or []:
        if row.get("type") == "micro" and row.get("band") in {"all", "short<=5", "long>5"}:
            out[row["band"]] = {
                "exact_p": row.get("exact_p"),
                "exact_r": row.get("exact_r"),
                "exact_f1": row.get("exact_f1"),
                "relaxed_f1": row.get("relaxed_f1"),
            }
    return out

def hist(path):
    p = path / "history.json"
    if not p.is_file():
        return None
    h = json.loads(p.read_text(encoding="utf-8"))
    return {"n_epochs": len(h), "last": h[-1] if h else None, "best_dev": max((x.get("dev_typed_f1") or -1) for x in h) if h else None}

rows = []
for name, d in arms.items():
    ev = d / "hybrid_eval.json"
    if not ev.is_file():
        rows.append({"name": name, "missing": str(ev)})
        continue
    j = json.loads(ev.read_text(encoding="utf-8"))
    h, g2 = j.get("v4_hybrid") or {}, j.get("gold_v2_side") or {}
    rows.append({
        "name": name,
        "status": "待验证",
        "scorer": h.get("scorer_version"),
        "alignment_ok": h.get("alignment_ok"),
        "n_gold": h.get("n_gold"),
        "n_matched": h.get("n_matched"),
        "n_missing": h.get("n_missing"),
        "snap": j.get("snap"),
        "typed_exact_p": h.get("typed_exact_p"),
        "typed_exact_r": h.get("typed_exact_r"),
        "typed_exact_f1": h.get("typed_exact_f1"),
        "typed_relaxed_f1": h.get("typed_relaxed_f1"),
        "collapsed_exact_f1": h.get("collapsed_exact_f1"),
        "gold_v2_exact_f1": g2.get("typed_exact_f1"),
        "gold_v2_alignment_ok": g2.get("alignment_ok"),
        "span_char5_micro": bands(j.get("span_char5_typed")),
        "history": hist(d),
    })

base = next((r for r in rows if r.get("name") == "vanilla_wwm_base" and "typed_exact_f1" in r), None)
large = next((r for r in rows if r.get("name") == "vanilla_wwm_large" and "typed_exact_f1" in r), None)
delta = None
if base and large:
    delta = (large["typed_exact_f1"] or 0) - (base["typed_exact_f1"] or 0)

out = {
    "status": "待验证",
    "not_for_confirmed_results": True,
    "gold_v2_untouched": True,
    "protocol": "V4 hybrid 2601 + jieba + cnss-lskt-1.2.0; read existing hybrid_eval.json",
    "ref_jobbert_confirmed": ref,
    "arms": rows,
    "delta_large_minus_base_exact": delta,
    "checks": {
        "both_alignment_ok": all(r.get("alignment_ok") is True for r in rows if "alignment_ok" in r),
        "both_n_gold_2601": all(r.get("n_gold") == 2601 for r in rows if "n_gold" in r),
        "both_n_missing_0": all(r.get("n_missing") in (0, None) for r in rows if "n_missing" in r),
    },
}
dst = PAPER / "output/vanilla_wwm_v4/pr_alignment_seed42.json"
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
print("wrote", dst)
PY
```

### 3c. 仅当某臂缺少 `hybrid_eval.json`、但有 `test_pred.jsonl` 时：CPU 重评

```bash
export SCESC_ROOT=/home/guojingli3/Chinese-Skillspan-Benchmark
export PYTHONPATH="$SCESC_ROOT/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
PY=/home/guojingli3/miniconda3/envs/adasparse/bin/python3
# 例：缺 base 的 hybrid_eval 时才跑这一行
# "$PY" "$SCESC_ROOT/Chinese_skill_benchmark_Paper/scripts/eval_one_hybrid_cws.py" \
#   --pred "$SCESC_ROOT/Chinese_skill_benchmark_Paper/output/vanilla_wwm_base_v4_silver_seed42/test_pred.jsonl" \
#   --out_dir "$SCESC_ROOT/Chinese_skill_benchmark_Paper/output/vanilla_wwm_base_v4_silver_seed42" \
#   --name vanilla_wwm_base
```

然后回到 3b。不要覆盖 Gold / silver。不要改 `test_pred.jsonl` 以外的输入。

### 3d. 回复格式（把这些贴回机 A 窗口）

用中文，先给表：

| 臂 | alignment_ok | n_gold | n_missing | exact P | exact R | exact F1 | relaxed F1 | Gold v2 exact（旁路） |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| vanilla base | | 2601? | | | | 0.4341? | | |
| vanilla large | | | | | | 0.4289? | | |
| JobBERT 3M（已确认） | — | 2601 | — | 0.4730 | 0.3994 | 0.4331 | 0.5873 | — |

再写四行：

1. 两臂 `alignment_ok` 是否都是 true，n 是否都是 2601，`n_filled_empty` / `n_missing` 是多少。
2. vanilla base 的 P/R 和 JobBERT 3M 的 0.4730 / 0.3994 是「同形状」还是明显偏 P 或偏 R。
3. `span_char5_micro` 的 short / long exact F1。
4. `history` 训了几 epoch、best_dev。

最后贴完整 `pr_alignment_seed42.json`（或两份 `hybrid_eval.json` 的 `v4_hybrid` + `snap` + `span_char5_typed` 里 micro 三行）。

不要把这些数写进 `confirmed-results.md`。不要开新训练。

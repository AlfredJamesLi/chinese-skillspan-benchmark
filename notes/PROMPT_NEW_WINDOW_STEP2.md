# 服务器 B 第二步（给新窗口贴）

第一步盘点已合格。下面只做：**建能看见 Blackwell 的 Python → 下 base+large 权重 → seed 42 两臂 CRF → jieba 评 hybrid**。  
不要对 Table 3 / 2676 / `admin_Baseline_test.jsonl` 复打分。不要找机 A 的 Slurm。不要写 abstract。

---

## PROMPT（第二步，贴到服务器 B 同一窗口）

第一步已完成，路径不要改。继续只做 vanilla WWM v4 CRF seed 42。

工作区：`/home/guojingli3/Chinese-Skillspan-Benchmark`  
软链已齐。空闲卡：**0, 3, 4, 5**（6/7 也可）。**不要用 GPU 1/2**。

### 不要做

- 不要用 `confirmed-results.md` 里 Table 3 / 2676 / `admin_Baseline_test.jsonl` 当本次金标。
- 不要跑 3-seed、large DAPT、Qwen/14B、repartition。
- 不要假设存在 `/opt/anaconda3/envs/adasparse/bin/python3`（那是机 A）。必须先确定本机 `PYTHON`。
- 数字未进机 A 的 `confirmed-results.md` 前一律 **待验证**。

### 2a. 环境（Blackwell 是最大风险）

```bash
WORK=/home/guojingli3/Chinese-Skillspan-Benchmark
export SCESC_ROOT="$WORK"
export PYTHONPATH="$WORK/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
# 找本机 python：miniconda / 已有 env。没有就建一个。
which python3; python3 -c "import sys; print(sys.executable)"
python3 -c "import torch,transformers,jieba,numpy; from torchcrf import CRF; print('torch', torch.__version__, 'cuda', torch.version.cuda, 'avail', torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO_CUDA')"
```

若 `import torch` 失败或 `cuda avail False` 或报 `sm_100` / `no kernel image`：用 miniconda 装带较新 CUDA 的 torch（优先 cu128/cu129），再装 `transformers jieba numpy`，`pip install -e "$WORK/Baseline_Models_Collection/pytorch-crf"`。装好后再测一次。  
通过后：`export PYTHON=$(which python3)`。后面脚本会读 `$PYTHON`。

### 2b. 下权重（包里没有）

```bash
export PYTHON="${PYTHON:-python3}"
# large
"$PYTHON" "$WORK/Chinese_skill_benchmark_Paper/scripts/download_cn_roberta_wwm_ext_large.py"
# base（脚本只下 large，这里下 base）
"$PYTHON" - << 'PY'
from pathlib import Path
from huggingface_hub import snapshot_download
dest = Path("/home/guojingli3/Chinese-Skillspan-Benchmark/Baseline_Models_Collection/chinese-roberta-wwm-ext")
if (dest/"config.json").is_file() and ((dest/"pytorch_model.bin").is_file() or (dest/"model.safetensors").is_file()):
    print("skip base", dest)
else:
    dest.mkdir(parents=True, exist_ok=True)
    try:
        snapshot_download("hfl/chinese-roberta-wwm-ext", local_dir=str(dest), ignore_patterns=["*.h5","tf_model*","flax*","*.msgpack"])
    except Exception as e:
        print("hf failed", e)
        snapshot_download("hfl/chinese-roberta-wwm-ext", local_dir=str(dest), endpoint="https://hf-mirror.com", ignore_patterns=["*.h5","tf_model*","flax*","*.msgpack"])
print("base ok", dest)
PY
ls -lh "$WORK/Baseline_Models_Collection/chinese-roberta-wwm-ext/pytorch_model.bin" \
      "$WORK/Baseline_Models_Collection/chinese-roberta-wwm-ext-large/pytorch_model.bin"
```

### 2c. 冒烟（GPU 0，只加载，不训满）

```bash
export CUDA_VISIBLE_DEVICES=0
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1
"$PYTHON" - << 'PY'
from transformers import AutoModel, AutoTokenizer
import torch
p="/home/guojingli3/Chinese-Skillspan-Benchmark/Baseline_Models_Collection/chinese-roberta-wwm-ext-large"
tok=AutoTokenizer.from_pretrained(p, local_files_only=True)
m=AutoModel.from_pretrained(p, local_files_only=True).cuda()
x=tok("测试", return_tensors="pt")
x={k:v.cuda() for k,v in x.items()}
y=m(**x)
print("smoke_ok", tuple(y.last_hidden_state.shape), torch.cuda.get_device_name(0))
PY
```

冒烟失败就停，把报错贴回来，不要开 6 epoch。

### 2d. 正式两臂（先串行，一张空闲卡）

```bash
export PYTHON
export SCESC_ROOT=/home/guojingli3/Chinese-Skillspan-Benchmark
export PYTHONPATH="$SCESC_ROOT/Baseline_Models_Collection/pytorch-crf:${PYTHONPATH:-}"
export CUDA_VISIBLE_DEVICES=0
export TRANSFORMERS_OFFLINE=1 HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false
# 脚本默认 python 是机 A 的 adasparse；必须覆盖
bash "$SCESC_ROOT/Chinese_skill_benchmark_Paper/scripts/run_vanilla_wwm_v4_crf.sh"
```

配方不要改：seed 42，epochs 6，patience 2，batch 16，max_len 256，lr 2e-5。  
若 OOM 再把 batch 降到 8 并写入 run.log，先不要改别的。96GB 一般 16 够。

可选加速（冒烟已过）：两张空闲卡并行，**不要改超参**。分别设 `CUDA_VISIBLE_DEVICES=0` 只跑 base、`=3` 只跑 large。做法：复制脚本逻辑，或先后台跑两次 `train_cn_roberta_crf.py`（`--model_dir` / `--out_dir` 不同），再各自 `eval_one_hybrid_cws.py`，最后用脚本末尾那段 compare。未并行成功就保持串行。

### 2e. 收工看哪个文件

- `Chinese_skill_benchmark_Paper/output/vanilla_wwm_base_v4_silver_seed42/hybrid_eval.json`
- `.../vanilla_wwm_large_v4_silver_seed42/hybrid_eval.json`
- `.../output/vanilla_wwm_v4/compare_seed42.json`

只报 **V4 hybrid typed exact**、delta、脚本写的 decision。标 **待验证**。  
停手：B−A < 0.015 或 B < 0.35 → 停。B−A ≥ 0.02 才提 3-seed。B ≥ 0.4272 才提 large DAPT。

做完把 `compare_seed42.json` 和两臂 exact 贴回这个窗口。

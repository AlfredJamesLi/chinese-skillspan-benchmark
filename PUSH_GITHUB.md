# GitHub 私有仓库备份

**状态：已推送**（2026-08-24）

- 仓库：https://github.com/AlfredJamesLi/chinese-skillspan-benchmark （private）
- 分支：`main`（与本地同步）
- 账号：`AlfredJamesLi`（`gh auth` 已登录）

本地 git 根目录：`Chinese_skill_benchmark_Paper/`（`main` 分支）。

## 已包含内容（约 16MB 压缩包 / 57MB 工作区）

- 代码：`scripts/`、`scorer/`
- 复现文档：`REPRO_GITHUB.md`、`HANDOFF.md`、`notes/`
- 核心数据：Gold v2、goldstyle train/dev、LSKT v4 SOP train/dev + `test_lskt_v4_rule_g2ids.jsonl`、corpus_splits（train/dev/test）
- 结果快照：`results_snapshots/`（各次 run_summary）
- 大文件清单：`data/LARGE_DATA_MANIFEST.md`

## 未包含（太大，见 LARGE_DATA_MANIFEST.md）

- `output/` 模型权重（53GB）
- `chineseskillspan-jobert-pretrain/` 原始 CSV/RAR（40GB）
- `jobbert_*_sents.jsonl` DAPT 语料（可用脚本重建）

## 步骤 1：登录 GitHub CLI

在**实验室服务器**或**本机**（若已 clone）执行：

```bash
export PATH="$HOME/.local/bin:$PATH"   # gh 已装在此路径
gh auth login
# 选：GitHub.com → HTTPS → Login with a web browser
```

## 步骤 2：创建私有仓库并推送

```bash
cd /home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper

gh repo create chinese-skillspan-benchmark \
  --private \
  --source=. \
  --remote=origin \
  --description "Chinese-SkillSpan benchmark: code, repro docs, core data (private backup)" \
  --push
```

若仓库名已被占用，改成例如 `chinese-skillspan-benchmark-private`。

## 步骤 3：验证

```bash
gh repo view --web
git remote -v
git log -1 --oneline
```

## 离线备份包（无需 GitHub 也可用）

已生成单文件 bundle，可拷到 U 盘 / 网盘：

```bash
# 文件位置
Chinese_skill_benchmark_Paper/chinese-skillspan-backup-main.bundle   # ~16MB

# 在另一台机器恢复
git clone chinese-skillspan-backup-main.bundle chinese-skillspan-benchmark
```

## 安全提醒

- 父仓库的 `api_key.py` **未**纳入本备份（已在 `.gitignore` 排除）。
- 推送前可再确认：`git log --stat | head` 与 `git grep -i sk-`（应无输出）。

## 后续更新

```bash
cd Chinese_skill_benchmark_Paper
git add -A
git status   # 确认无 output/ 大文件
git commit -m "Update backup"
git push origin main
```

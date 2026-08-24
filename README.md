# Chinese-SkillSpan Benchmark — 论文工作区

本目录是 **Chinese-SkillSpan / Chinese Skill Benchmark** 文的准备区（数据集文，arXiv `2604.23009`）。  
不要把 IEEE Access / SRICL 方法文写进这里。

当前窗口在实验服务器仓库内。本机 Overleaf 另开窗口时，把 `overleaf_cursor_bundle/` 拷到 Overleaf Git 根目录。

## 目录

| 路径 | 用途 |
|---|---|
| `pdf/` | **把最新稿 PDF 放到这里**（文件名建议带日期，如 `draft_2026-08-22.pdf`） |
| `notes/` | 从 PDF / 实验里抽出的主张、待填数字、冲突表 |
| `tex/` | 服务器上的草稿 `.tex`（尚未从 Overleaf 同步时用） |
| `tables/` | 表源（`.tex` / `.csv`） |
| `figs/` | 图 |
| `HANDOFF.md` | 本窗口完整交接（先读这个） |
| `overleaf_cursor_bundle/` | 拷到本机 Overleaf 仓库的规则 / skill / 交接 |

## 本窗口先做什么

1. 把最新 PDF 上传到 `pdf/`。
2. 让助手对照 PDF 填写 `notes/confirmed-results.md` 和 `overleaf_cursor_bundle/.cursor/skills/cnss-overleaf/confirmed-results.md`。
3. 再改 `tex/` 或准备 Overleaf 同步包。未写入「已确认」的数字不要写进论文。

## GitHub 私有备份

本目录已初始化为独立 git 仓库（代码 + 复现文档 + 核心数据，不含 40GB+ 预训练原始文件）。

- 复现说明：`REPRO_GITHUB.md`
- 大文件清单：`data/LARGE_DATA_MANIFEST.md`
- **推送到 GitHub（需一次性登录）：`PUSH_GITHUB.md`**
- 离线包：`chinese-skillspan-backup-main.bundle`（~16MB）

实验数据与流水线仍在父仓库（只读备查，不要当成本目录的一部分去改 Access 文稿）：

- 数据：`chinese_skillspan_preprocessing/`
- 推理入口：父目录 `main.py`、`prompt_template_rag.py`
- 中文 LoRA：`LLaMA-Factory/saves/.../sft_CN_skillspan_*`
- Access 文稿：`access_paper/` — **不要改**

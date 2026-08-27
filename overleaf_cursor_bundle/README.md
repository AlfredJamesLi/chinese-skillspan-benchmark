# 把本包拷进本机 Overleaf 仓库（Chinese-SkillSpan）

完整交接：`HANDOVER_OVERLEAF.md`。新 Overleaf 窗口应先 `@HANDOVER_OVERLEAF.md`。

## 1. 拷贝（本机 PowerShell）

把交接文件和 `.cursor` 拷到 **Overleaf Git 仓库根**（不要多一层 `overleaf_cursor_bundle`）：

```powershell
$src = "从服务器下载后的 overleaf_cursor_bundle 路径"
$dst = "本机 Overleaf 仓库根路径"
Copy-Item "$src\HANDOVER_OVERLEAF.md" "$dst\HANDOVER_OVERLEAF.md" -Force
Copy-Item "$src\AGENTS.md" "$dst\AGENTS.md" -Force
Copy-Item "$src\CODEX_PROMPT_ALL.md" "$dst\CODEX_PROMPT_ALL.md" -Force
Copy-Item "$src\CODEX_PROMPT_PROTOCOL_CONSULT.md" "$dst\CODEX_PROMPT_PROTOCOL_CONSULT.md" -Force
Copy-Item "$src\CODEX_PROMPT_HANDBOOK.md" "$dst\CODEX_PROMPT_HANDBOOK.md" -Force
Copy-Item "$src\handbooks" "$dst\handbooks" -Recurse -Force
Copy-Item "$src\tables" "$dst\tables" -Recurse -Force
Copy-Item "$src\.cursor" "$dst\.cursor" -Recurse -Force
Copy-Item "$src\CHAT_SEED.txt" "$dst\CHAT_SEED.txt" -Force
```

服务器路径：

`/home/guojingli3/SCESC-LLM-skill-extraction/Chinese_skill_benchmark_Paper/overleaf_cursor_bundle/`

## 2. 用 Cursor 打开 Overleaf 仓库

File → Open Folder → 本机 Overleaf 克隆（不要开 `access_paper/overleaf_cursor_bundle`，那是 SRICL / IEEE Access）。

## 3. 新对话粘贴 `CHAT_SEED.txt`

第一句必须是先读交接。

## 4. 文件分工

| 文件 | 角色 |
|---|---|
| `HANDOVER_OVERLEAF.md` | 完整交接（先读） |
| `AGENTS.md` | 窗口身份 |
| `CODEX_PROMPT_HANDBOOK.md` | 先咨询手册 A/B 如何写入 Methods（不改 tex） |
| `CODEX_PROMPT_ALL.md` | 给 Codex 的合并改稿提示词（整段粘贴） |
| `CODEX_PROMPT_PROTOCOL_CONSULT.md` | 咨询新旧协议表结构（不改 tex） |
| `handbooks/` | 手册 A（Gold v2）/ 手册 B（SOP v4）各一页，中英 |
| `.cursor/skills/cnss-overleaf/confirmed-results.md` | 已确认数字 |
| `.cursor/skills/cnss-overleaf/not-for-paper.md` | 禁写清单 |
| `tables/` | Overleaf 用 CSV（Gold v2 / encoder / 分域） |
| 服务器 `Chinese_skill_benchmark_Paper/HANDOFF.md` | 服务器窗口用；本机改 tex 以本包交接为准 |

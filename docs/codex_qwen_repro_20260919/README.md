# Codex handoff: Qwen reproduction zip (2026-09-19)

Cursor export for Codex on a laptop that cannot SSH to servers A/B.  
This directory is documentation only. The zip is a **GitHub pre-release asset**, not git, not Zenodo v0.1.3.

**This GitHub pre-release is a transfer channel, not a CC-BY grant on adapters or advertisements.**

## Download into Windows Downloads

Release tag: `qwen-repro-pack-20260919`  
Repo: `AlfredJamesLi/chinese-skillspan-benchmark`  
Do not use Latest (that remains `v0.1.3`).

```bat
gh release download qwen-repro-pack-20260919 -R AlfredJamesLi/chinese-skillspan-benchmark -D %USERPROFILE%\Downloads
certutil -hashfile %USERPROFILE%\Downloads\CNSS_Qwen_Reproduction.zip SHA256
```

Direct asset URL (public):

https://github.com/AlfredJamesLi/chinese-skillspan-benchmark/releases/download/qwen-repro-pack-20260919/CNSS_Qwen_Reproduction.zip

| Field | Value |
|---|---|
| Bytes | 865168457 |
| SHA256 | `e1098b42fdf6302b451152530449f5c9666d7cd44a829189b7434988634709e8` |

Then read `LICENSE_NOTICE.md` and `CONTENTS_NOTE.md` in this folder (also inside the zip). Gold150 freeze sentences are in the zip; expanded-silver train jsonl is not. Leave Zenodo v0.1.3 untouched. New Zenodo record only.

Prompt: `CODEX_PROMPT_QWEN_REPRO_ZENODO_20260919.md`

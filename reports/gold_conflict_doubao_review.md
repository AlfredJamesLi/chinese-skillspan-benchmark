# Doubao 18-conflict check (human review)

Date: 2026-08-22. Model: 豆包 (first LLM pass).  
A/B were Gold **file duplicates**, not dual annotators.

Guideline used: only candidate competency; no 报名/公示/体检/资格审查流程.

| id | Doubao | Review | Proposed Gold spans |
|---|---|---|---|
| 1987-s0045 | 试讲[S] 答辩[S] | **Revise → empty**. Same sentence is exam format; Doubao left 笔试 empty on 1988-s0085. 试讲/答辩 here are interview links, not a job skill list. | `[]` |
| 1987-s0059 | empty | Accept | `[]` |
| 1988-s0026 | 普通高等教育全日制大学专科以上学历[K] | Accept. Drop 户籍/退役士兵. | `(37,54,K)` |
| 1988-s0027 | empty | Accept | `[]` |
| 1988-s0063 | empty | Accept | `[]` |
| 1988-s0085 | empty | Accept (exam timetable). 医学类 as K is optional; sentence is 参加…笔试. | `[]` |
| 1988-s0107 | 理论素养[K] + five T | Accept. 综合分析 as T (not S). 语言表达能力 as T (old export used S). | token spans as Doubao |
| 1988-s0113 | 学历[K] | **Revise → empty**. Tie-break rule after 并列, not a hiring competency. Parallel to empty 成绩. | `[]` |
| 1988-s0154 | empty | Accept | `[]` |
| 1988-s0161 | empty | Accept | `[]` |
| 1989-s0001 | empty | Accept | `[]` |
| 1989-s0023 | empty | Accept | `[]` |
| 1991-s0006 | 良好的品行和职业道德[T] | Accept | `(4,14,T)` |
| 1991-s0033 | empty | Accept | `[]` |
| 1991-s0042 | 医学专业[K]; 从事乡村医生工作[S]; 《乡村医生执业证书》[K] | **Revise**. 「有意愿从事」is intent not skill. 免试注册证书 is post-hire procedure. Keep major only. | `(12,16,K)` 医学专业 |
| 1995-s0036 | empty | Accept | `[]` |
| 1995-s0037 | empty | Accept | `[]` |
| 1999-s0072 | empty | Accept | `[]` |

Confirmed by user 2026-08-22: use this review as human Gold (15 Doubao accepts + 3 revisions).
Written into `data/gold_canonical_v2.jsonl`.


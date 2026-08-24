#!/usr/bin/env python3
"""Locked empty-sentence hints. Does not write Gold v2 or train.json."""
from __future__ import annotations

import re

PROCESS = re.compile(
    r"(网上报名|报名时间|报考|准考证|资格审查|资格复审|资格审核|"
    r"笔试时间|面试时间|面试安排|体检|公示|本公告|招聘公告|"
    r"咨询电话|联系电话|请登录|下载报名|岗位代码|招聘人数|"
    r"免责声明|未尽事宜|解释权|工作地点[:：]|报名入口)"
)
WELFARE = re.compile(
    r"(五险一金|带薪年假|包吃|包住|加班费|班次|双休|福利待遇|"
    r"节日福利|定期体检|提供宿舍|缴纳社保)"
)
ABILITY = re.compile(r"(熟悉|掌握|了解|精通|具备|具有|学历|专业|能力|经验|证书|英语|普通话)")


def empty_hint(sentence: str, domain: str) -> str:
    s = sentence or ""
    d = domain or ""
    if PROCESS.search(s) and not ABILITY.search(s):
        return "empty_process"
    if WELFARE.search(s) and not ABILITY.search(s):
        return "empty_welfare"
    if d == "事业单位招聘" and PROCESS.search(s):
        return "empty_shiye_process"
    if d == "事业单位招聘" and not ABILITY.search(s) and len(s) <= 40:
        return "review_shiye_maybe_empty"
    return ""

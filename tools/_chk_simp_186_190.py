# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

SIMP = re.compile(
    r"[这说们来对为时过还发经与从开关问头条样种点动体实应该认识绪选练脑处进机无个会东车马风龙门头干干干干"
    r"产现长国医乐亲儿气复疗伤创历观视录转变买卖难单价质盘损仓场账钱买卖录图报际计设读写语号码库级类区线"
    r"击扩摊获论护优势败负责务称总额费资债润亏险证汇预测档页链结构层维运营销购储备复杂简显隐稳变换转递迟达远"
    r"贝态频宽窄涨跌创闭锁钥扫描识别离职银联团组织训练试验状况环戏剧众连专义词编辑译导检监]"
)
# More targeted simplified chars commonly mistaken
SIMP2 = set("这为个说会对发后还与让从当经现点时样种们语请该术尔里干干干只只只只只只只只只只只只只只只只只只")
# Better explicit list
CHARS = "这为个说会对发还与让从当经现点时样种们语请该术尔后里干只台台台"

files = list(Path("tools").glob(".findbook_results_grok_02_psychology_growth-20260717-18[6-9].json"))
files += list(Path("tools").glob(".findbook_results_grok_02_psychology_growth-20260717-190.json"))
for p in files:
    data = json.loads(p.read_text(encoding="utf-8"))
    print("==", data["id"], len(data["highlights"]))
    for i, line in enumerate(data["highlights"], 1):
        hits = [ch for ch in line if ch in "这为个说会对发还与让从当经现点时样种们语请该术尔后里干台只"]
        # filter known OK: 台 in 台灣/台階下, 后 in 皇后? 里 as 這裡?
        if hits:
            print(f"  {i:03d} {hits} {line[:40]}")

#!/usr/bin/env python3
"""video-craft-playbook 维护工具：status / brief / new-case / check / close / consolidate。只用标准库。"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "references"
CASES = ROOT / "cases"
INBOX = CASES / "inbox"
ARCHIVE = CASES / "archive"
LEDGER = CASES / "LEDGER.md"
ATLAS = REFS / "capability-atlas.md"
LESSONS = REFS / "craft-lessons.md"
PITFALLS = REFS / "pitfalls.md"
PATTERNS = REFS / "composition-patterns.md"
BACKLOG = REFS / "lessons-backlog.md"

CARD_FIELDS = ["产出", "擅长的表达", "边界", "确定性", "代价", "接口", "入口", "验证"]
STALE_DAYS = 90
FIELD_WARN, FIELD_FAIL = 400, 600
MAX_LESSONS, MAX_GENERAL, MAX_PATTERN_LINES = 60, 25, 12
ENTRY_WARN, CHECKPOINT_WARN = 300, 15
CONSOLIDATE_AT, BACKLOG_STALE_DAYS, CONSOLIDATE_CASES, RECENT_CASES = 15, 60, 5, 10
QUOTA = {"craft-lessons.md": 2, "pitfalls.md": 3, "composition-patterns.md": 1}
EXPERIENCE = ["craft-lessons.md", "pitfalls.md", "lessons-backlog.md"]
BIASED = re.compile(
    r"默认(选|用|走|路线|方案|工具)|首选|推荐|优先(选|用|使用|考虑)|最佳(工具|方案|选择)|一律(用|选|走)"
)
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
CARD_ID = re.compile(r"^([A-H]\d+) ")
OVERVIEW_ROW = re.compile(r"^\| ([A-H]\d+) \| ", re.M)
LESSON_ID = re.compile(r"^- \*\*L(\d+) ", re.M)
LESSON_REF = re.compile(r"(?:craft-lessons|lessons-backlog) L(\d+)")
PHASES = ["规划", "执行", "审片", "交付"]
TAG_VOCAB = {
    "歌词MV": "歌词 MV、唱段对口型",
    "产品片": "产品发布、宣传、界面演示",
    "预告片": "预告片、把既有素材剪成短版",
    "讲解片": "解说、科普、口播",
    "复刻": "按参考片、参考图或类型片复刻",
    "模板": "参数化模板、批量出片",
    "画风": "指定艺术风格或画家风格",
    "生成": "生成视频或图像素材",
    "3D": "3D 资产、Blender、程序化 3D 渲染",
    "three.js": "three.js 场景",
    "物理": "物理模拟、参数搜索",
    "网页渲染": "Remotion、HyperFrames 等浏览器逐帧渲染",
    "运动模糊": "需要真运动模糊",
    "抠像": "matte、遮罩、抠出主体",
    "遮幅": "宽银幕遮幅、活动区",
    "素材检索": "找真实素材、开放素材库",
    "配乐": "配乐、卡点、用户指定音乐",
    "配音": "TTS、人声、对白",
    "音效": "事件音效、拟音",
    "ffmpeg": "ffmpeg 剪辑、封装、转码脚本",
    "付费": "付费调用",
    "弱模型": "较弱或便宜的模型来做",
    "对比实验": "同题多模型或有无手册对比",
}
TAG_BLOCK = re.compile(r"〔(通用|条件：([^｜〕]+))｜([^〕]+)〕")
GROUP_TAG = re.compile(r"〔([^｜〕]+)(?:｜上限 (\d+))?〕\s*$")
CARD_COLUMNS = ["起作用", "适用但漏用", "照做但误导", "不适用"]
CARD_REF = re.compile(r"(?<![A-Za-z0-9-])L(\d+)")
LAST_CONSOLIDATED = re.compile(r"上次归纳：(\d{4}-\d{2}-\d{2})")


def today():
    return dt.date.today()


def atlas_cards():
    """返回 [(标题, {字段: 内容})]。"""
    cards, title, fields = [], None, {}
    for line in ATLAS.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") or line.startswith("### "):
            if title:
                cards.append((title, fields))
            title, fields = (line[4:].strip(), {}) if line.startswith("### ") else (None, {})
            continue
        m = re.match(r"- \*\*(.+?)\*\*[：:](.*)", line)
        if title and m:
            fields[m.group(1)] = m.group(2).strip()
    if title:
        cards.append((title, fields))
    return cards


def stale_cards():
    out = []
    for title, f in atlas_cards():
        dates = DATE.findall(f.get("验证", ""))
        if dates:
            age = (today() - dt.date.fromisoformat(max(dates))).days
            if age > STALE_DAYS:
                out.append((title, age))
    return out


def lesson_ids(path=None):
    path = path or LESSONS
    return [int(n) for n in LESSON_ID.findall(path.read_text(encoding="utf-8"))] if path.exists() else []


def backlog_entries():
    """返回候补层 [(行号, 行, 最早日期或 None, 所在分节)]；“常驻条目细则”分节不参与晋升与阈值。"""
    out, section = [], None
    if BACKLOG.exists():
        for i, l in enumerate(BACKLOG.read_text(encoding="utf-8").splitlines(), 1):
            if l.startswith("## "):
                section = l[3:].strip()
            if section and l.startswith("- "):
                dates = DATE.findall(l)
                out.append((i, l, min(dates) if dates else None, section))
    return out


def backlog_candidates():
    return [e for e in backlog_entries() if "细则" not in e[3]]


def backlog_age(entries_):
    ages = [(today() - dt.date.fromisoformat(e[2])).days for e in entries_ if e[2]]
    return max(ages) if ages else 0


def entries(path):
    return [l for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("- ")]


def split_tags(s):
    return {t for t in re.split(r"[、,，\s]+", s.strip()) if t}


def lessons(path=None):
    """经验条目 [{id, line, no, tagged, general, tags, phases}]；候补层只取“经验候补”分节。"""
    path = path or LESSONS
    out, sec = [], None
    if not path.exists():
        return out
    for i, l in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if l.startswith("## "):
            sec = l[3:].strip()
        m = LESSON_ID.match(l)
        if not m or (path == BACKLOG and sec != "经验候补"):
            continue
        t = TAG_BLOCK.search(l)
        out.append({"id": int(m.group(1)), "line": l, "no": i, "tagged": bool(t),
                    "general": bool(t) and t.group(1) == "通用",
                    "tags": split_tags(t.group(2)) if t and t.group(2) else set(),
                    "phases": split_tags(t.group(3)) if t else set()})
    return out


def pitfall_groups(path):
    """坑分组 [[标题, 标签, 上限或 None, [条目]]]：pitfalls 用 ## 分组，候补层用“坑候补”下的 ### 分组。"""
    level = "### " if path == BACKLOG else "## "
    out, cur, inside = [], None, path != BACKLOG
    if not path.exists():
        return out
    for l in path.read_text(encoding="utf-8").splitlines():
        if path == BACKLOG and l.startswith("## "):
            inside, cur = l[3:].strip() == "坑候补", None
            continue
        if not inside:
            continue
        if l.startswith(level):
            m = GROUP_TAG.search(l)
            cur = [GROUP_TAG.sub("", l[len(level):]).strip(), split_tags(m.group(1)) if m else set(),
                   int(m.group(2)) if m and m.group(2) else None, []]
            out.append(cur)
        elif cur and l.startswith("- "):
            cur[3].append(l)
    return out


def detail_lines():
    """候补层“常驻条目细则”：{L 号: 行}。"""
    out, sec = {}, None
    for l in BACKLOG.read_text(encoding="utf-8").splitlines() if BACKLOG.exists() else []:
        if l.startswith("## "):
            sec = l[3:].strip()
        m = re.match(r"- \*\*细则 L(\d+)。", l)
        if m and sec == "常驻条目细则":
            out[int(m.group(1))] = l
    return out


def card_usage():
    """归档案例卡“用到的手册条目”：[(日期, slug, {栏: {L 号}})]；不在四栏里的行记为“旧格式引用”。"""
    out = []
    for p in sorted(ARCHIVE.glob("*.md")) if ARCHIVE.exists() else []:
        m = re.search(r"^## 用到的手册条目\n(.*?)(?=^## |\Z)", p.read_text(encoding="utf-8"), re.S | re.M)
        cols = {}
        body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S) if m else ""
        for line in body.splitlines():
            c = re.match(r"- (" + "|".join(CARD_COLUMNS) + r")[：:](.*)", line)
            ids = {int(n) for n in CARD_REF.findall(c.group(2) if c else line)}
            if ids:
                cols.setdefault(c.group(1) if c else "旧格式引用", set()).update(ids)
        out.append((p.stem[:10], p.stem[11:], cols))
    return out


def last_consolidated():
    m = LAST_CONSOLIDATED.search(BACKLOG.read_text(encoding="utf-8")) if BACKLOG.exists() else None
    return m.group(1) if m else None


def cases_since(day):
    done = re.findall(r"\| 已蒸馏 (\d{4}-\d{2}-\d{2}) \|", LEDGER.read_text(encoding="utf-8"))
    # 台账只记到日：归纳当天关闭的案例也计入（宁可多提醒一次，也不让归纳当天之后关闭的案例永远不计数）
    return sum(1 for d in done if day is None or d >= day)


def pattern_sections():
    """返回 [(案例标题, 正文行数)]，只数 ### 案例。"""
    out, title, n = [], None, 0
    for line in PATTERNS.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            if title:
                out.append((title, n))
            title, n = line[4:].strip(), 0
        elif line.startswith("## "):
            if title:
                out.append((title, n))
            title = None
        elif title and line.strip():
            n += 1
    if title:
        out.append((title, n))
    return out


def cmd_status(_):
    inbox = sorted(INBOX.glob("*.md")) if INBOX.exists() else []
    print(f"手册位置：{ROOT}")
    if inbox:
        print(f"⚠ 待蒸馏案例 {len(inbox)} 条（先按 references/writeback.md 蒸馏再开新片）：")
        for p in inbox:
            print(f"  - {p.name}")
    else:
        print("✓ 没有待蒸馏的案例卡")
    stale = stale_cards()
    if stale:
        print(f"⚠ 超过 {STALE_DAYS} 天未复核的能力卡 {len(stale)} 张（用到时顺手核验并更新验证日期）：")
        for t, age in stale:
            print(f"  - {t}（{age} 天）")
    bl = backlog_candidates()
    last = last_consolidated()
    since = cases_since(last)
    if bl or since:
        oldest = backlog_age(bl)
        due = len(bl) >= CONSOLIDATE_AT or oldest > BACKLOG_STALE_DAYS or since >= CONSOLIDATE_CASES
        print(f"{'⚠' if due else '·'} 候补层 {len(bl)} 条，最老 {oldest} 天；上次归纳 {last or '无记录'} 以来关闭 {since} 个案例"
              + ("（到归纳阈值，跑 `playbook.py consolidate`）" if due else ""))
    print("· 规划、执行、审片、交付各阶段开始时跑 `playbook.py brief --phase <阶段> --tags <标签>`，标签词表 `brief --list-tags`")
    rows = [l for l in LEDGER.read_text(encoding="utf-8").splitlines() if re.match(r"\| \d{4}-", l)]
    if rows:
        print(f"台账共 {len(rows)} 条，最近：{rows[-1]}")
    return 0


def cmd_new_case(a):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.slug):
        sys.exit("slug 只用小写字母、数字和连字符")
    INBOX.mkdir(parents=True, exist_ok=True)
    d = today().isoformat()
    path = INBOX / f"{d}-{a.slug}.md"
    if any(q.stem[11:] == a.slug for q in INBOX.glob("*.md")):
        sys.exit(f"已存在同名案例卡：{a.slug}")
    title = (a.title or a.slug).replace("|", "/")
    tpl = (CASES / "TEMPLATE.md").read_text(encoding="utf-8")
    path.write_text(tpl.format(slug=a.slug, date=d, title=title), encoding="utf-8")
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(f"| {d} | {a.slug} | {title} | inbox | 待蒸馏 |\n")
    print(f"已创建 {path}")
    return 0


def link_targets(path):
    out = []
    for target in LINK.findall(path.read_text(encoding="utf-8")):
        if "://" not in target:
            out.append((path.parent / target).resolve())
    return out


def cmd_check(_):
    errors, warns = [], []
    cards = atlas_cards()
    for title, f in cards:
        missing = [k for k in CARD_FIELDS if not f.get(k)]
        if missing:
            errors.append(f"能力卡「{title}」缺字段：{'、'.join(missing)}")
        elif not DATE.search(f["验证"]):
            errors.append(f"能力卡「{title}」的“验证”缺少核验日期")
        for k, v in f.items():
            if len(v) > FIELD_FAIL:
                errors.append(f"能力卡「{title}」的“{k}”{len(v)} 字符，超过 {FIELD_FAIL}，清单改指针、实现移工作区")
            elif len(v) > FIELD_WARN:
                warns.append(f"能力卡「{title}」的“{k}”{len(v)} 字符，超过 {FIELD_WARN}")
    card_ids = {m.group(1) for t, _ in cards for m in [CARD_ID.match(t)] if m}
    overview_ids = set(OVERVIEW_ROW.findall(ATLAS.read_text(encoding="utf-8")))
    for cid in sorted(card_ids - overview_ids):
        errors.append(f"能力卡 {cid} 不在总览表里")
    for cid in sorted(overview_ids - card_ids):
        errors.append(f"总览表里的 {cid} 没有对应能力卡")
    for t, age in stale_cards():
        warns.append(f"能力卡「{t}」{age} 天未复核")
    docs = [ROOT / "SKILL.md", *sorted(REFS.glob("*.md"))]
    for md in sorted(REFS.glob("*.md")):
        if md.name == "writeback.md":
            continue
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if "neutral-ok" in line:
                continue
            m = BIASED.search(line)
            if m:
                errors.append(f"{md.name}:{i} 带倾向性措辞「{m.group(0)}」，改成条件句")
    linked = set()
    for md in docs:
        for target in link_targets(md):
            if not target.exists():
                errors.append(f"{md.name} 链接不可达：{target.name}")
            linked.add(target)
    for md in sorted(REFS.glob("*.md")):
        if md.resolve() not in linked:
            errors.append(f"references/{md.name} 没有被任何文件链接（新文件需用户确认并接入）")
    ids = lesson_ids()
    all_ids = ids + lesson_ids(BACKLOG)
    for n in sorted({n for n in all_ids if all_ids.count(n) > 1}):
        errors.append(f"craft-lessons / lessons-backlog L{n} 编号重复")
    for md in docs:
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            for n in LESSON_REF.findall(line):
                if int(n) not in all_ids:
                    errors.append(f"{md.name}:{i} 引用的 L{n} 在 craft-lessons 与 lessons-backlog 都不存在")
    if len(ids) > MAX_LESSONS:
        errors.append(f"craft-lessons {len(ids)} 条，超过上限 {MAX_LESSONS}，先合并或移出")
    resident = lessons()
    for label, group in (("craft-lessons", resident), ("lessons-backlog", lessons(BACKLOG))):
        for e in group:
            where = f"{label} L{e['id']}"
            if not e["tagged"]:
                errors.append(f"{where} 缺适用面与阶段标签〔通用｜阶段〕或〔条件：标签｜阶段〕")
                continue
            bad = sorted((e["tags"] - TAG_VOCAB.keys()) | (e["phases"] - set(PHASES)))
            if bad or not e["phases"]:
                errors.append(f"{where} 标签不在词表里：{'、'.join(bad) or '缺阶段'}（词表见 brief --list-tags）")
    general = [e for e in resident if e["general"]]
    if len(general) > MAX_GENERAL:
        errors.append(f"craft-lessons 通用条目 {len(general)} 条，超过 {MAX_GENERAL}：新条目要胜过最弱的通用条目才能进，否则标条件")
    pits = entries(PITFALLS)
    for path in (PITFALLS, BACKLOG):
        for title, tags, cap, items in pitfall_groups(path):
            bad = sorted(tags - TAG_VOCAB.keys())
            if not tags or bad:
                errors.append(f"{path.name}「{title}」分组缺工具标签或标签不在词表里：{'、'.join(bad)}")
            if path == PITFALLS and cap is None:
                errors.append(f"pitfalls「{title}」分组标题缺“上限 N”")
            elif path == PITFALLS and len(items) > cap:
                errors.append(f"pitfalls「{title}」{len(items)} 条，超过本组上限 {cap}，先合并或移出")
    for day, slug, cols in card_usage():
        for col, ns in cols.items():
            for n in sorted(ns - set(all_ids)):
                warns.append(f"案例卡 {slug}「{col}」引用的 L{n} 不存在")
    for title, n in pattern_sections():
        if n > MAX_PATTERN_LINES:
            errors.append(f"composition-patterns「{title}」{n} 行，超过 {MAX_PATTERN_LINES} 行")
    for name in EXPERIENCE:
        if not (REFS / name).exists():
            continue
        in_section = name != "lessons-backlog.md"
        for i, line in enumerate((REFS / name).read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## "):
                in_section = True
            if not in_section or not line.startswith("- "):
                continue
            if "（" not in line:
                warns.append(f"{name}:{i} 没有来源案例")
            size = len(TAG_BLOCK.sub("", line))
            if name != "lessons-backlog.md" and size > ENTRY_WARN:
                warns.append(f"{name}:{i} 单条 {size} 字符（不计标签），超过 {ENTRY_WARN}，归纳时拆成一句结论 + 候补细节")
    ledger = LEDGER.read_text(encoding="utf-8")
    for p in sorted(INBOX.glob("*.md")) if INBOX.exists() else []:
        slug = p.stem[11:]
        if f"| {slug} |" not in ledger:
            errors.append(f"inbox 卡 {p.name} 未登记台账")
    for w in warns:
        print(f"warn  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        print(f"check 未通过：{len(errors)} 处")
        return 1
    print(f"check 通过（能力卡 {len(cards)} 张，经验 {len(ids)} 条（通用 {len(general)}/{MAX_GENERAL}），"
          f"坑 {len(pits)} 条（常驻层各组未超上限）、坑候补 {sum(len(g[3]) for g in pitfall_groups(BACKLOG))} 条，warn {len(warns)}）")
    return 0


def cmd_close(a):
    cards = [q for q in INBOX.glob("*.md") if q.stem[11:] == a.slug] if INBOX.exists() else []
    if not cards:
        sys.exit(f"inbox 里没有 {a.slug}")
    card = cards[0]
    text = card.read_text(encoding="utf-8")
    sec = text.split("## 蒸馏去向", 1)[-1]
    body = re.sub(r"<!--.*?-->", "", sec, flags=re.S).strip()
    if not body:
        sys.exit("“蒸馏去向”还没填写：写明改了哪些文件，或“无新知识：<原因>”")
    if cmd_check(None) != 0:
        sys.exit("先修好 check 的问题再 close")
    for name, quota in QUOTA.items():
        lines = (REFS / name).read_text(encoding="utf-8").splitlines()
        n = sum(1 for l in lines if (l.startswith("- ") or l.startswith("### ")) and a.slug in l)
        if n > quota:
            print(f"warn  {name} 含本案例 {n} 处，超过每案配额 {quota}；理由应写在案例卡“蒸馏去向”")
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    card.write_text(text.replace("status: inbox", "status: distilled", 1), encoding="utf-8")
    card.rename(ARCHIVE / card.name)
    first = [l.strip().lstrip("-* ").strip() for l in body.splitlines() if l.strip()]
    summary = (first[0] + "；".join(first[1:]) if first[0].endswith("：") else first[0]).replace("|", "/")
    lines = LEDGER.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if f"| {a.slug} |" in line and "| inbox |" in line:
            cols = line.split("|")
            cols[4] = f" 已蒸馏 {today().isoformat()} "
            cols[5] = f" {summary} "
            lines[i] = "|".join(cols)
    LEDGER.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已归档 {ARCHIVE / card.name}，台账已更新")
    return 0


def fmt_counts(counter):
    return "、".join(f"L{n}×{c}" for n, c in counter.most_common()) or "无"


def cmd_consolidate(_):
    from collections import Counter
    print("归纳清单（只读，不改文件；处理顺序：删被推翻的 → 合并同主题 → 拆长条 → 晋升与降级 → 组内按价值排序 → check → 更新候补层“上次归纳”日期）")
    bl = backlog_candidates()
    det = len(backlog_entries()) - len(bl)
    usage = card_usage()
    recent = usage[-RECENT_CASES:]
    others = "\n".join(p.read_text(encoding="utf-8") for p in [ROOT / "SKILL.md", *REFS.glob("*.md")] if p != BACKLOG)
    print(f"1. 候补层 {len(bl)} 条（晋升条件见 writeback 第一节第 4 条）：")
    for i, l, d, _ in bl:
        m = LESSON_ID.match(l)
        tag = f"L{m.group(1)}" if m else "坑"
        refs = len(re.findall(rf"lessons-backlog L{m.group(1)}\b", others)) if m else 0
        worked = [s for _, s, cols in usage if m and int(m.group(1)) in cols.get("起作用", set()) and s not in l]
        age = (today() - dt.date.fromisoformat(d)).days if d else -1
        flag = f"  ← 可晋升：非来源案例记为起作用（{'、'.join(worked)}）" if worked else ""
        print(f"   - :{i} {tag}  {age} 天  被其他文件引用 {refs} 处  {TAG_BLOCK.sub('', l).replace('**  ', '** ')[:40]}…{flag}")
    print(f"   另有常驻条目细则 {det} 条（下沉的细节，不参与晋升）")
    long_ = []
    for name in ("craft-lessons.md", "pitfalls.md"):
        for i, l in enumerate((REFS / name).read_text(encoding="utf-8").splitlines(), 1):
            if l.startswith("- ") and len(TAG_BLOCK.sub("", l)) > ENTRY_WARN:
                long_.append((name, i, len(TAG_BLOCK.sub("", l))))
    print(f"2. 常驻层超过 {ENTRY_WARN} 字的条目 {len(long_)} 条（拆成一句结论 + 候补细节或工作区指针）：")
    for name, i, n in long_:
        print(f"   - {name}:{i}  {n} 字")
    res = lessons()
    gen = [e for e in res if e["general"]]
    print(f"3. 容量：经验 {len(res)}/{MAX_LESSONS}（通用 {len(gen)}/{MAX_GENERAL}）；晋升进满员的层要一进一出")
    print("   坑：" + "；".join(f"{t} {len(items)}/{cap}" for t, _, cap, items in pitfall_groups(PITFALLS)))
    print("   坑候补：" + ("；".join(f"{t} {len(items)} 条" for t, _, _, items in pitfall_groups(BACKLOG)) or "无"))
    print("   各阶段通用条目：" + "、".join(f"{p} {sum(p in e['phases'] for e in gen)}" for p in PHASES)
          + f"（加上命中的条件与候补条目，每个检查点 ≤ {CHECKPOINT_WARN} 条为宜）")
    col = lambda name, cards: Counter(n for _, _, c in cards for n in c.get(name, set()))
    print(f"4. 案例卡计数（共 {len(usage)} 张，近 {len(recent)} 张；四栏新格式 + 旧格式引用；零次不是删除信号）：")
    print("   适用但漏用（改阶段标签或挂到检查点，不降级）：" + fmt_counts(col("适用但漏用", usage)))
    print("   照做但误导（降级候选，先核实证据）：" + fmt_counts(col("照做但误导", usage)))
    notapp = col("不适用", recent)
    weak = Counter({e["id"]: notapp[e["id"]] for e in gen if notapp[e["id"]] >= 5})
    print("   通用条目近案记“不适用” ≥ 5 次（改标条件的候选）：" + fmt_counts(weak))
    used = col("起作用", recent) + col("旧格式引用", recent)
    print(f"   常驻经验近案使用次数：{fmt_counts(Counter({n: c for n, c in used.items() if n in {e['id'] for e in res}}))}；"
          f"未出现 {sum(1 for e in res if e['id'] not in used)} 条")
    last = last_consolidated()
    print(f"5. 节奏：上次归纳 {last or '无记录'}，此后关闭 {cases_since(last)} 个案例；"
          f"阈值：候补 ≥ {CONSOLIDATE_AT} 条、最老 > {BACKLOG_STALE_DAYS} 天、或关闭 ≥ {CONSOLIDATE_CASES} 个案例，先到者为准")
    return 0


def cmd_brief(a):
    res, cand, det = lessons(), lessons(BACKLOG), detail_lines()
    if a.list_tags:
        groups = pitfall_groups(PITFALLS) + pitfall_groups(BACKLOG)
        print("阶段：" + "、".join(PHASES))
        print("条件标签（括号里是经验 / 候补 / 坑的条数）：")
        for t, d in TAG_VOCAB.items():
            n3 = sum(len(items) for _, tags, _, items in groups if t in tags)
            print(f"  {t}：{d}（{sum(t in e['tags'] for e in res)} / {sum(t in e['tags'] for e in cand)} / {n3}）")
        return 0
    if not a.phase:
        sys.exit("用 --phase 指定阶段：" + "、".join(PHASES))
    tags = split_tags(a.tags or "")
    if tags - TAG_VOCAB.keys():
        sys.exit(f"不在词表里的标签：{'、'.join(sorted(tags - TAG_VOCAB.keys()))}；词表见 brief --list-tags")
    hit = lambda e: a.phase in e["phases"] and (e["general"] or bool(e["tags"] & tags))
    general = [e for e in res if e["general"] and hit(e)]
    cond = [e for e in res if not e["general"] and hit(e)]
    cands = [e for e in cand if hit(e)]
    print(f"brief：阶段 {a.phase}；标签 {'、'.join(sorted(tags)) or '无（只列通用条目）'}")

    def show(title, items, note=""):
        if not items:
            return
        print(f"\n【{title}】{len(items)} 条{note}")
        for e in items:
            print(e["line"])
            if e["id"] in det:
                print(f"  ↳ {det[e['id']]}" if a.details else "  ↳ 有细则：加 --details 一并列出")

    show("通用", general)
    show("条件", cond)
    show("候补", cands, "（单一来源或只有外部证据，用前自己判断；用了在案例卡里记一笔）")
    if a.phase == "执行" and tags:
        for path, label in ((PITFALLS, "坑"), (BACKLOG, "坑候补")):
            for title, gtags, _, items in pitfall_groups(path):
                if gtags & tags and items:
                    print(f"\n【{label}·{title}】{len(items)} 条")
                    print("\n".join(items))
    k = len(general) + len(cond) + len(cands)
    print(f"\n本检查点经验 {k} 条" + (f"；超过 {CHECKPOINT_WARN} 条，标签给宽了，或这些条目该合并" if k > CHECKPOINT_WARN else ""))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    b = sub.add_parser("brief", help="按阶段与标签列出该检查点要照做的条目")
    b.add_argument("--phase", choices=PHASES)
    b.add_argument("--tags", help="逗号或顿号分隔，词表见 --list-tags")
    b.add_argument("--details", action="store_true", help="一并列出细则")
    b.add_argument("--list-tags", action="store_true")
    b.set_defaults(fn=cmd_brief)
    n = sub.add_parser("new-case")
    n.add_argument("slug")
    n.add_argument("--title")
    n.set_defaults(fn=cmd_new_case)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    sub.add_parser("consolidate").set_defaults(fn=cmd_consolidate)
    c = sub.add_parser("close")
    c.add_argument("slug")
    c.set_defaults(fn=cmd_close)
    a = p.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()

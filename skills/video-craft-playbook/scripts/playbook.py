#!/usr/bin/env python3
"""video-craft-playbook 维护工具：status / new-case / check / close。只用标准库。"""

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
MAX_LESSONS, MAX_PITFALLS, MAX_PATTERN_LINES = 60, 60, 12
ENTRY_WARN, CONSOLIDATE_AT, BACKLOG_STALE_DAYS = 300, 10, 90
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
    if bl:
        oldest = backlog_age(bl)
        due = len(bl) >= CONSOLIDATE_AT or oldest > BACKLOG_STALE_DAYS
        print(f"{'⚠' if due else '·'} 候补层 {len(bl)} 条，最老 {oldest} 天" + ("（到归纳阈值，跑 `playbook.py consolidate`）" if due else ""))
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
    pits = entries(PITFALLS)
    if len(pits) > MAX_PITFALLS:
        errors.append(f"pitfalls {len(pits)} 条，超过上限 {MAX_PITFALLS}，先合并或移出")
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
            if name != "lessons-backlog.md" and len(line) > ENTRY_WARN:
                warns.append(f"{name}:{i} 单条 {len(line)} 字符，超过 {ENTRY_WARN}，归纳时拆成一句结论 + 候补细节")
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
    print(f"check 通过（能力卡 {len(cards)} 张，经验 {len(ids)} 条，坑 {len(pits)} 条，warn {len(warns)}）")
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


def cmd_consolidate(_):
    print("归纳清单（只读，不改文件；处理顺序：删被推翻的 → 合并同主题 → 拆长条 → 晋升 → check）")
    bl = backlog_candidates()
    det = len(backlog_entries()) - len(bl)
    others = "\n".join(p.read_text(encoding="utf-8") for p in [ROOT / "SKILL.md", *REFS.glob("*.md")] if p != BACKLOG)
    print(f"1. 候补层 {len(bl)} 条（晋升条件：两个不同案例的来源，或推翻常驻层说法）：")
    for i, l, d, _ in bl:
        m = LESSON_ID.match(l)
        tag = f"L{m.group(1)}" if m else ("细则" if l.startswith("- **细则") else "坑")
        refs = len(re.findall(rf"lessons-backlog L{m.group(1)}\b", others)) if m else 0
        age = (today() - dt.date.fromisoformat(d)).days if d else -1
        print(f"   - :{i} {tag}  {age} 天  被其他文件引用 {refs} 处  {l[:40]}…")
    print(f"   另有常驻条目细则 {det} 条（下沉的细节，不参与晋升）")
    long_ = []
    for name in ("craft-lessons.md", "pitfalls.md"):
        for i, l in enumerate((REFS / name).read_text(encoding="utf-8").splitlines(), 1):
            if l.startswith("- ") and len(l) > ENTRY_WARN:
                long_.append((name, i, len(l)))
    print(f"2. 常驻层超过 {ENTRY_WARN} 字的条目 {len(long_)} 条（拆成一句结论 + 候补细节或工作区指针）：")
    for name, i, n in long_:
        print(f"   - {name}:{i}  {n} 字")
    cards = "\n".join(p.read_text(encoding="utf-8") for p in ARCHIVE.glob("*.md")) if ARCHIVE.exists() else ""
    used = {int(n) for n in re.findall(r"\bL(\d+)\b", cards)}
    unused = [n for n in lesson_ids() if n not in used]
    print(f"3. 常驻层容量：经验 {len(lesson_ids())}/{MAX_LESSONS}，坑 {len(entries(PITFALLS))}/{MAX_PITFALLS}；晋升一条就要合并或移出一条")
    print(f"4. 从未被归档案例卡引用的经验 {len(unused)} 条（使用信号，不是删除指令；案例卡“用到的手册条目”一节写得越全越准）：L" + "、L".join(map(str, unused)))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status").set_defaults(fn=cmd_status)
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

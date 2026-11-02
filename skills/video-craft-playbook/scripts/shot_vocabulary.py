#!/usr/bin/env python3
"""从 video-shotcraft 的 gallery/api/library.json 重新生成 references/shot-vocabulary.md 的卡片索引段。

用法：python3 scripts/shot_vocabulary.py <video-shotcraft 仓库路径>
只替换 <!-- generated:start --> 与 <!-- generated:end --> 之间的内容，标记外的手写段落不动。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "references" / "shot-vocabulary.md"
ORDER = ["opening", "camera", "transition", "typography", "ui-entrance", "interaction", "data", "effects", "rhythm", "outro"]
ENERGY_RANK = {"低": 0, "中": 1, "高": 2}
INNER_PAREN = re.compile(r"[（(][^（）()]*[）)]")


def strip_parens(text: str) -> str:
    while INNER_PAREN.search(text):
        text = INNER_PAREN.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def clip(text: str, limit: int) -> str:
    """在 limit 内最后一个逗号或分号处截断；找不到就硬截加省略号。"""
    if len(text) <= limit:
        return text
    cut = max(text.rfind(ch, 0, limit) for ch in "，；、")
    return text[:cut] if cut >= limit // 2 else text[: limit - 1] + "…"


def summary(text: str, limit: int = 46) -> str:
    text = strip_parens(text)
    if "——" in text:
        name, rest = text.split("——", 1)
        text = f"{name}：{rest}" if len(name) <= 14 else name
    return clip(text, limit).replace("|", "/")


def energy(text: str) -> str:
    return clip(strip_parens(text).replace(" ", ""), 9)


def energy_key(text: str) -> float:
    head = re.split(r"[/；，]", strip_parens(text))[0]
    if "极" in head or "峰" in head:
        return 3
    ranks = [ENERGY_RANK[ch] for ch in head if ch in ENERGY_RANK]
    return sum(ranks) / len(ranks) if ranks else 1


def main(repo: Path) -> int:
    lib = json.loads((repo / "gallery" / "api" / "library.json").read_text(encoding="utf-8"))
    try:
        commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001 - 仓库不是 git 时只省略提交号
        commit = "unknown"
    labels = lib.get("categories") or {}
    cards = sorted(lib["cards"], key=lambda c: (ORDER.index(c["category"]) if c["category"] in ORDER else 99, -energy_key(c["energy"]), c["name"]))
    lines = [f"来源：video-shotcraft `library.json` revision {lib.get('revision')}，仓库提交 {commit}；{lib['stats'].get('cardCount', len(cards))} 卡 / {lib['stats'].get('styleCount', '')} 式；卡片最近更新 {lib['stats'].get('newest', '')[:10]}。", ""]
    cur = None
    for c in cards:
        if c["category"] != cur:
            cur = c["category"]
            label = labels.get(cur, {}).get("zh", cur)
            n = sum(1 for x in cards if x["category"] == cur)
            lines += ["", f"### {cur} · {label}（{n} 卡）", "", "| 卡名 | 能量 | 时长 | 一句话 | 式 |", "|---|---|---|---|---|"]
        styles = len(c.get("styles") or [])
        dur = clip(strip_parens(c.get("duration", "")), 16)
        lines.append(f"| `{c['name']}` | {energy(c.get('energy', ''))} | {dur} | {summary(c.get('summary', ''))} | {styles if styles > 1 else ''} |")
    generated = "\n".join(lines).strip() + "\n"
    text = OUT.read_text(encoding="utf-8")
    start, end = "<!-- generated:start -->", "<!-- generated:end -->"
    if start not in text or end not in text:
        sys.exit(f"{OUT} 缺少 {start} / {end} 标记")
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    OUT.write_text(f"{head}{start}\n{generated}{end}{tail}", encoding="utf-8")
    print(f"已写入 {OUT}（{len(cards)} 卡）")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(Path(sys.argv[1]).expanduser().resolve()))

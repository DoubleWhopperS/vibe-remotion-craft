#!/usr/bin/env python3
"""下载 search.py 结果里选中的一条，并追加到 <项目>/assets/manifest.json。

用法：
  python3 -I download.py <results.json> <id> --shot "S1 暴雨落在路口" --project <项目目录> [--note "..."]
manifest 每条：file、sha256、bytes、source、source_id、title、page_url、download_url、author、author_url、
license、license_url、attribution_required、downloaded_at、used_for、query、filters、notes。
同一 source + id 重复下载时只更新 used_for，不重复下文件。只用标准库。
"""
import argparse, datetime as dt, hashlib, json, os, pathlib, re, sys, urllib.parse, urllib.request

UA = "asset-discovery-poc/0.1 (local video research; python urllib)"
REQUIRED = ["file", "source", "source_id", "page_url", "download_url", "author", "license", "license_url",
            "downloaded_at", "used_for"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results")
    ap.add_argument("id")
    ap.add_argument("--shot", required=True, help="用于哪一镜")
    ap.add_argument("--project", required=True)
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    doc = json.load(open(a.results, encoding="utf-8"))
    hit = next((r for r in doc["results"] if str(r["id"]) == a.id), None)
    if not hit:
        sys.exit(f"{a.results} 里没有 id={a.id}")
    assets = pathlib.Path(a.project, "assets")
    assets.mkdir(parents=True, exist_ok=True)
    mpath = assets / "manifest.json"
    manifest = json.load(open(mpath, encoding="utf-8")) if mpath.exists() else []
    old = next((m for m in manifest if m["source"] == hit["source"] and str(m["source_id"]) == a.id), None)
    if old:
        if a.shot not in old["used_for"]:
            old["used_for"].append(a.shot)
        json.dump(manifest, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"已在 manifest：{old['file']}，used_for → {old['used_for']}")
        return
    ext = pathlib.PurePosixPath(urllib.parse.urlparse(hit["download_url"]).path).suffix or ".bin"
    name = f"{hit['source']}-{a.id}{ext}"
    dest = assets / name
    req = urllib.request.Request(hit["download_url"], headers={"User-Agent": UA})
    h, n = hashlib.sha256(), 0
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        for chunk in iter(lambda: r.read(1 << 20), b""):
            f.write(chunk); h.update(chunk); n += len(chunk)
    entry = {"file": f"assets/{name}", "sha256": h.hexdigest(), "bytes": n,
             "source": hit["source"], "source_id": hit["id"], "title": hit.get("title"),
             "page_url": hit["page_url"], "download_url": hit["download_url"],
             "author": hit.get("author"), "author_url": hit.get("author_url"),
             "license": hit.get("license"), "license_url": hit.get("license_url"),
             "attribution_required": hit.get("attribution_required"),
             "media": hit.get("media"), "width": hit.get("width"), "height": hit.get("height"),
             "duration": hit.get("duration"),
             "downloaded_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
             "used_for": [a.shot], "query": doc.get("query"), "filters": doc.get("filters"), "notes": a.note}
    missing = [k for k in REQUIRED if not entry.get(k)]
    if missing:
        print(f"warn  manifest 缺字段：{'、'.join(missing)}，交付前补齐（打开 page_url 核对）", file=sys.stderr)
    manifest.append(entry)
    json.dump(manifest, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{dest}  {n/1e6:.1f} MB  {entry['license']}  {entry['author']}")


if __name__ == "__main__":
    main()

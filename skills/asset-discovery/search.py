#!/usr/bin/env python3
"""开放素材库检索：把镜头描述翻成的检索词发给各库，结果统一成同一组字段。

用法：
  python3 -I search.py <源> "<检索词>" [筛选] [--out results.json]
源：
  openverse-image / openverse-audio   匿名
  commons-video / commons-image       匿名（Wikimedia Commons）
  pexels-video                        需 PEXELS_API_KEY
  pixabay-video                       需 PIXABAY_API_KEY
  freesound-audio                     需 FREESOUND_API_KEY（API 条款：仅限非商用；下载链接为 128 kbps 预览）
key 只读环境变量（建议用密钥管理器注入），例如：
  python3 -I search.py pexels-video "flooded street"
只用标准库。输出 JSON：{source, query, filters, fetched_at, quota, results[]}，results 每项字段见 norm()。
"""
import argparse, datetime as dt, html, json, os, re, sys, urllib.error, urllib.parse, urllib.request

UA = "asset-discovery-poc/0.1 (local video research; python urllib)"
TIMEOUT = 90  # Openverse 检索端点实测 50–60 s 才返回（2026-10-31）


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        quota = {k: v for k, v in r.headers.items() if "ratelimit" in k.lower()}
        return json.load(r), quota


def need_key(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"待 key：环境变量 {name} 不存在，先注入该环境变量再运行 {sys.argv[0]}。")
    return v


def norm(**kw):
    keys = ["source", "id", "title", "page_url", "download_url", "media", "width", "height",
            "duration", "fps", "author", "author_url", "license", "license_url",
            "attribution_required", "thumbnail", "tags", "signals"]
    return {k: kw.get(k) for k in keys}


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def openverse(kind, q, a):
    p = {"q": q, "page_size": a.n, "mature": "false"}
    if a.license: p["license"] = a.license
    if a.commercial: p["license_type"] = "commercial,modification"
    if kind == "images":
        if a.orientation: p["aspect_ratio"] = {"landscape": "wide", "portrait": "tall", "square": "square"}[a.orientation]
        if a.min_width: p["size"] = "large"
    url = f"https://api.openverse.org/v1/{kind}/?" + urllib.parse.urlencode(p)
    try:
        d, quota = get(url)
    except (urllib.error.URLError, TimeoutError) as e:
        # 新检索词首次常要 26–60 s，超过网关 60 s 回 5xx；后端仍会算完并缓存，重试一次通常 1–30 s 返回（2026-10-31 实测）
        if isinstance(e, urllib.error.HTTPError) and e.code < 500: raise
        print(f"# openverse 首次请求失败（{getattr(e, 'code', '') or e}），重试一次", file=sys.stderr)
        d, quota = get(url)
    out = []
    for r in d.get("results", []):
        out.append(norm(source="openverse-image" if kind == "images" else "openverse-audio", id=r["id"], title=r.get("title"),
                        page_url=r.get("foreign_landing_url"), download_url=r.get("url"),
                        media="image" if kind == "images" else "audio",
                        width=r.get("width"), height=r.get("height"),
                        duration=(r.get("duration") or 0) / 1000 or None,
                        author=r.get("creator"), author_url=r.get("creator_url"),
                        license=f"{r.get('license', '').upper()} {r.get('license_version') or ''}".strip(),
                        license_url=r.get("license_url"),
                        attribution_required=r.get("license") not in ("cc0", "pdm"),
                        thumbnail=r.get("thumbnail"), tags=[t["name"] for t in r.get("tags") or []][:12]))
    return out, quota, d.get("result_count")


def commons(kind, q, a):
    sq = f"{q} filetype:{'video' if kind == 'video' else 'bitmap'}"
    p = {"action": "query", "format": "json", "generator": "search", "gsrsearch": sq, "gsrnamespace": 6,
         "gsrlimit": a.n, "prop": "imageinfo|videoinfo",
         "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 480,
         "viprop": "derivatives", "iiextmetadatafilter": "LicenseShortName|LicenseUrl|Artist|AttributionRequired|UsageTerms"}
    d, quota = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p))
    total = None
    out = []
    pages = sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda x: x.get("index", 0))
    for pg in pages:
        ii = (pg.get("imageinfo") or [{}])[0]
        em = {k: strip(v.get("value")) for k, v in (ii.get("extmetadata") or {}).items()}
        url, w, h = ii.get("url"), ii.get("width"), ii.get("height")
        if kind == "video":
            # 原片常是 4K webm：给了 --min-width 挑最小够用的转码版本，没给挑最大的
            ders = sorted([x for x in (pg.get("videoinfo") or [{}])[0].get("derivatives", []) if x.get("width")],
                          key=lambda x: x["width"])
            ok = [x for x in ders if x["width"] >= a.min_width] if a.min_width else ders[-1:]
            if ok: url, w, h = ok[0]["src"], ok[0]["width"], ok[0]["height"]
            elif a.min_width and (w or 0) < a.min_width: continue
        lic = em.get("LicenseShortName", "")
        if a.commercial and not re.search(r"public domain|cc0|cc[- ]by(?![- ]nc)", lic, re.I): continue
        out.append(norm(source=f"commons-{kind}", id=pg["pageid"], title=pg["title"],
                        page_url=ii.get("descriptionurl"), download_url=url, media=kind,
                        width=w, height=h, duration=ii.get("duration"),
                        author=em.get("Artist"), license=lic, license_url=em.get("LicenseUrl") or ii.get("descriptionurl"),
                        attribution_required=em.get("AttributionRequired", "true") != "false",
                        thumbnail=ii.get("thumburl")))
    return out, quota, total


def pexels(q, a):
    key = need_key("PEXELS_API_KEY")
    p = {"query": q, "per_page": a.n}
    if a.orientation: p["orientation"] = a.orientation
    if a.min_dur: p["min_duration"] = int(a.min_dur)
    if a.max_dur: p["max_duration"] = int(a.max_dur)
    d, quota = get("https://api.pexels.com/v1/videos/search?" + urllib.parse.urlencode(p), {"Authorization": key})
    out = []
    for v in d.get("videos", []):
        files = sorted([f for f in v["video_files"] if f.get("width") and f["width"] >= (a.min_width or 0)],
                       key=lambda f: f["width"]) or v["video_files"]
        f = files[0]
        out.append(norm(source="pexels-video", id=v["id"], title=v.get("url", "").rstrip("/").split("/")[-1],
                        page_url=v.get("url"), download_url=f["link"], media="video",
                        width=f.get("width"), height=f.get("height"), duration=v.get("duration"), fps=f.get("fps"),
                        author=v["user"]["name"], author_url=v["user"]["url"],
                        license="Pexels License", license_url="https://www.pexels.com/license/",
                        attribution_required=False, thumbnail=v.get("image")))
    return out, quota, d.get("total_results")


def pixabay(q, a):
    key = need_key("PIXABAY_API_KEY")
    p = {"key": key, "q": q, "per_page": max(3, a.n), "safesearch": "true"}
    if a.min_width: p["min_width"] = a.min_width
    d, quota = get("https://pixabay.com/api/videos/?" + urllib.parse.urlencode(p))
    out = []
    for h in d.get("hits", []):
        if a.min_dur and h["duration"] < a.min_dur: continue
        if a.max_dur and h["duration"] > a.max_dur: continue
        vs = sorted([v for v in h["videos"].values() if v.get("url") and v["width"] >= (a.min_width or 0)],
                    key=lambda v: v["width"]) or [v for v in h["videos"].values() if v.get("url")]
        v = vs[0]
        out.append(norm(source="pixabay-video", id=h["id"], title=h.get("tags"), page_url=h["pageURL"],
                        download_url=v["url"], media="video", width=v["width"], height=v["height"],
                        duration=h["duration"], author=h["user"],
                        author_url=f"https://pixabay.com/users/{h['user']}-{h['user_id']}/",
                        license="Pixabay Content License", license_url="https://pixabay.com/service/license-summary/",
                        attribution_required=False, thumbnail=v.get("thumbnail"), tags=h.get("tags", "").split(", ")))
    return out, quota, d.get("totalHits")


FS_LICENSE = {  # Freesound 返回许可名；URL 按其站内说明对应（新上传为 4.0，老条目可能是 3.0，以 page_url 为准）
    "Creative Commons 0": ("CC0 1.0", "https://creativecommons.org/publicdomain/zero/1.0/"),
    "Attribution": ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
    "Attribution NonCommercial": ("CC BY-NC 4.0", "https://creativecommons.org/licenses/by-nc/4.0/"),
}
FS_LICENSE_ARG = {"cc0": "Creative Commons 0", "by": "Attribution", "by-nc": "Attribution NonCommercial"}


def fs_license(raw):
    """返回 (标签, URL, 是否需署名)。实测 API 返回的是许可 URL（2026-11-02 冒烟），文档写的是名称，两种都接。"""
    if raw.startswith("http"):
        m = re.search(r"/(publicdomain/zero|licenses/[a-z-]+)/(\d\.\d)", raw)
        kind, ver = (m.group(1), m.group(2)) if m else (raw, "")
        cc0 = kind == "publicdomain/zero"
        label = f"CC0 {ver}" if cc0 else f"CC {kind.split('/')[-1].upper()} {ver}"
        return label.strip(), raw, not cc0
    label, url = FS_LICENSE.get(raw, (raw, None))
    return label, url, raw != "Creative Commons 0"


def freesound(q, a):
    key = need_key("FREESOUND_API_KEY")
    flt = []
    if a.min_dur or a.max_dur:
        flt.append(f"duration:[{a.min_dur or 0} TO {a.max_dur or '*'}]")
    lic = [FS_LICENSE_ARG[x] for x in (a.license or "").split(",") if x in FS_LICENSE_ARG]
    if a.commercial and not lic:
        lic = ["Creative Commons 0", "Attribution"]  # 素材许可允许商用；API 本身的使用条款仍限非商用，见 README
    if lic:
        flt.append("license:(" + " OR ".join(f'"{x}"' for x in lic) + ")")
    p = {"query": q, "page_size": max(3, a.n), "fields": "id,name,description,username,license,duration,"
         "num_downloads,avg_rating,num_ratings,previews,url,tags,type,samplerate,channels"}
    if flt: p["filter"] = " ".join(flt)
    d, quota = get("https://freesound.org/apiv2/search/?" + urllib.parse.urlencode(p),
                   headers={"Authorization": f"Token {key}"})
    out = []
    for h in d.get("results", []):
        lic_label, lic_url, attr = fs_license(h.get("license") or "")
        prev = h.get("previews") or {}
        desc = strip(h.get("description"))
        out.append(norm(source="freesound-audio", id=h["id"], title=h.get("name"), page_url=h.get("url"),
                        download_url=prev.get("preview-hq-mp3"), media="audio", duration=h.get("duration"),
                        author=h.get("username"), author_url=f"https://freesound.org/people/{h.get('username')}/",
                        license=lic_label, license_url=lic_url, attribution_required=attr,
                        tags=h.get("tags"),
                        signals={"downloads": h.get("num_downloads"), "rating": h.get("avg_rating"),
                                 "ratings": h.get("num_ratings"), "type": h.get("type"),
                                 "samplerate": h.get("samplerate"), "channels": h.get("channels"),
                                 "description": desc[:300]}))
    return out, quota, d.get("count")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", choices=["openverse-image", "openverse-audio", "commons-video", "commons-image",
                                       "pexels-video", "pixabay-video", "freesound-audio"])
    ap.add_argument("query")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--orientation", choices=["landscape", "portrait", "square"])
    ap.add_argument("--min-width", type=int)
    ap.add_argument("--min-dur", type=float)
    ap.add_argument("--max-dur", type=float)
    ap.add_argument("--license", help="Openverse / Freesound 许可筛选，如 cc0,by（Freesound 另有 by-nc）")
    ap.add_argument("--commercial", action="store_true", help="只要允许商用且可修改的")
    ap.add_argument("--out")
    a = ap.parse_args()
    s = a.source
    try:
        if s.startswith("openverse"): res, quota, total = openverse("images" if s.endswith("image") else "audio", a.query, a)
        elif s.startswith("commons"): res, quota, total = commons(s.split("-")[1], a.query, a)
        elif s == "pexels-video": res, quota, total = pexels(a.query, a)
        elif s == "freesound-audio": res, quota, total = freesound(a.query, a)
        else: res, quota, total = pixabay(a.query, a)
    except (urllib.error.URLError, TimeoutError) as e:  # 库端超时、5xx、401/429 都在这里，换库或稍后重试
        sys.exit(f"{s} 请求失败：{getattr(e, 'code', '')} {getattr(e, 'reason', e)}")
    doc = {"source": s, "query": a.query,
           "filters": {k: v for k, v in vars(a).items() if k not in ("source", "query", "out") and v},
           "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
           "total": total, "quota": quota, "results": res}
    if a.out:
        json.dump(doc, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for r in res:
        dur = f"{r['duration']:.1f}s" if r["duration"] else "-"
        size = f"{r['width']}x{r['height']}" if r["width"] else "-"
        sig = r.get("signals") or {}
        extra = f"\t↓{sig.get('downloads')} ★{sig.get('rating') or 0:.1f}({sig.get('ratings')})" if sig else ""
        print(f"{r['id']}\t{size}\t{dur}\t{r['license']}\t{(r['title'] or '')[:70]}{extra}")
    print(f"# {s} '{a.query}': {len(res)} 条（库内总数 {total}）quota={quota}", file=sys.stderr)


if __name__ == "__main__":
    main()

# asset-discovery：开放素材库检索、下载与来源记录

来源：asset-discovery-poc（2026-10-30）。链路见 video-craft-playbook craft-lessons L60、atlas H1。

文案 → 镜头描述（主体、动作、环境、景别、运镜、时长、画幅、色调）→ 英文检索词 → `search.py` → 看缩略图与每秒联系表、标可用区间 → `download.py` 写 `assets/manifest.json` → `conform_grade.py` 统一规格与调色 → 合成 → `check_frames.py` 逐帧核验。

## 脚本

| 文件 | 用途 |
|---|---|
| `search.py` | `python3 -I search.py <源> "<检索词>" [--min-width 1280] [--orientation landscape] [--min-dur 5] [--commercial] [--n 15] [--out r.json]`。源：`openverse-image`、`openverse-audio`、`commons-video`、`commons-image`（匿名），`pexels-video`、`pixabay-video`、`freesound-audio`（要 key）。结果统一成 id、宽高、时长、作者、许可证与链接、缩略图；速率限制响应头记进 `quota`。Freesound 另带 `signals`（下载量、评分均值与人数、格式、采样率、描述前 300 字），stdout 多一列 `↓下载 ★评分(人数)`，选材时看人数多的评分而不是均值高的（思路来自 vibe-motion/sound） |
| `download.py` | `python3 -I download.py r.json <id> --shot "S1 …" --project <项目>`：下到 `<项目>/assets/<源>-<id>.<ext>`，追加 manifest（file、sha256、bytes、source、source_id、title、page_url、download_url、author、author_url、license、license_url、attribution_required、downloaded_at、used_for、query、filters、notes）；同一条再登记只追加 used_for；必填字段缺失会 warn |
| `conform_grade.py` | 案例脚本副本：按 `timeline.ts` 的 SHOTS 裁区间 → 1920×1080@30（`setpts=PTS-STARTPTS` 后再 `fps`，多读 0.3 s 截整段，否则 VFR 源少 1 帧、`minterpolate` 吃尾部 2 帧）→ 以第一镜为参考做 Lab 均值方差迁移出 17³ `.cube`，ffmpeg `lut3d` 套到其他镜；输出均值 ΔE 与重复帧数 |
| `mixkit_search.py` | `python3 -I mixkit_search.py <slug> --out r.json [--n 24]`：Mixkit 无 API，抓公开检索页与详情页，逐条读下载区 `data-license`，只有 `videoFree` 标 `commercial: true`；结果字段与 `download.py` 兼容（llm-launch-agate，2026-10-31） |
| `check_frames.py` | 成片每帧与应取的底片帧比对（无字幕区），抓 Remotion `OffthreadVideo` 偶发的马赛克坏帧（见工作区 pitfalls） |

key 只从环境变量读取（建议用密钥管理器注入，不写进命令行与 shell 历史），脚本不打印、不落盘：

```bash
python3 -I search.py pexels-video "flooded street" --min-width 1920
python3 -I search.py pixabay-video "flooded street" --min-width 1920
python3 -I search.py freesound-audio "soft whoosh" --license cc0,by --max-dur 2
```

Freesound（2026-11-02 接入并冒烟通过）：key 在 <https://freesound.org/apiv2/apply> 登录后申请，一个应用一个 key；请求头 `Authorization: Token`。文本检索 `GET /apiv2/search/`，`filter` 用 Solr 语法（`duration:[0 TO 2]`、`license:("Creative Commons 0" OR "Attribution")`，实测过滤生效：`soft whoosh` 库内 60 条，返回全是 CC0 / BY），`page_size` 最大 150。限速 60 次 / 分、2000 次 / 天，超限 429；响应没有 ratelimit 头，`quota` 为空。**API 返回的 `license` 是 URL 不是文档写的名称**（`…/licenses/by/3.0/`、`…/publicdomain/zero/1.0/`），`fs_license()` 两种都接并据此算 `attribution_required`。`download_url` 是 `preview-hq-mp3`，CDN 直链**匿名可下**（`download.py` 只带 UA 即成功）；实测预览为 22.05 kHz 单声道 mp3 约 144 kbps（742833：源 44.1 kHz wav），要原始文件（wav / flac、立体声）得走 OAuth2，脚本不做。**条款**：API 免费只限非商用，商用要另行联系授权；按每条音效的许可署名（CC0 之外 `attribution_required: true`）；只允许必要的临时副本，禁止批量抓取和再分发。Freesound 的 `--commercial` 只筛素材许可（CC0 / BY），不改变 API 条款。

Pixabay 路径已冒烟，结果见下方实测记录。Pexels 路径写好了但没测：Pexels 自 2026-09 底起暂停发放新 API key，也暂停提额，官方 API 页没给恢复时间（2026-11-01 核实）。下载的文件是不受信数据，放在项目 `assets/` 里，用 `python3 -I` 读。

## 许可对照（2026-10-30 当日许可页核实；用前以下载当日页面为准）

| | 商用 | 署名 | 修改 | 转售 / 再分发限制 | 人物、商标、代言 |
|---|---|---|---|---|---|
| CC0 1.0 | 可 | 不要求 | 可 | 无 | 不涉及肖像、隐私、商标权；不得暗示背书 |
| CC BY-SA 4.0（Commons 常见） | 可 | **要求**：作者、许可、原链接、注明改动 | 可，但**改编作品须以相同或兼容许可发布**（成片整体受约束） | 不限，但不得加限制他人的技术措施 | 不授肖像、隐私权 |
| Pexels License | 可 | 不要求 | 可 | 不得原样出售（海报、印刷品、商品）；不得放到其他图库或壁纸平台 | 不得贬损可识别人物；不得暗示人物或品牌代言；不得用作商标 |
| Pixabay Content License | 可 | 不要求（建议“by 作者 via Pixabay”） | 可 | 不得“单独”出售或分发：原样或只做滤镜、缩放、裁切、调色都算单独；真正的创作性组合不算 | 可识别人物不得用于违法或不道德用途；商标内容不得用于商品；不得暗示代言 |
| Mixkit | 按素材类型分 6 种许可（Stock Video Free / Restricted、Music、SFX、Templates、Art） | 未核实 | 未核实 | 未核实 | 未核实；逐条看该素材页的 “View License” |

API 层规则（官方文档，2026-10-30）：
- Pexels：200 次/小时、2 万次/月，`X-Ratelimit-*` 头计数；使用 API 要求在界面显眼处链接 Pexels，尽量署名摄影师。
- Pixabay：每个 key 100 次/60 s，超限 429；检索结果须缓存 24 小时；不许永久盗链，要下载到自己这边；不许系统化批量下载，条款禁止抓取。
- Openverse：匿名限额文档没给数字，响应头实测为 20 次/分钟、200 次/天（2026-10-31）。新检索词首次请求常要 26–60 s，超过网关 60 s 回 500 / 504；后端仍会算完并缓存，同一请求再发通常 1–30 s 返回。`search.py` 超时 90 s，5xx 或超时自动重试一次。2026-10-30 记的“连续 504”就是这个现象。2026-10-31 图片、音频各检索并下载 1 条，manifest 与 sha256 核对通过。
- Wikimedia Commons：匿名 `api.php`，要带描述性 User-Agent。许可按文件逐条不同，`--commercial` 只保留 PD / CC0 / CC BY / CC BY-SA，`attribution_required` 取自页面元数据。视频给了 `--min-width` 挑最小够用的转码版本，没给挑最大的转码版本（2026-10-31 前没给时会挑到 240p）。

## 实测记录（asset-discovery-poc，2026-10-30）

- 检索词：Commons 视频，同一意图下 “城市 内涝” 0 条、“暴雨 街道” 1 条（新闻片，带烧录字幕与台标）；“flooded street” 9 条、“heavy rain street” 13 条（≥1280 宽、可商用）。
- 命中质量：9 个看过的候选里 4 个可用；2 条新闻片带烧录字幕，1 条 4:3 加黑边，1 条航拍内容偏离；Commons 视频多为手机拍摄，常见 VFR（29.495 fps）和 25 fps。
- 调色：第二镜（布法罗，偏黄 b* 8.99）对第一镜（蒙特利尔，b* 1.32）做 Lab 迁移，方差只迁 80%，两镜均值 ΔE 11.17 → 0.94。
- 帧率：25 → 30 直接 `fps` 会每 6 帧重复 1 帧（210 帧中 35 帧）；`minterpolate` 补帧后重复帧为 0，水花段原有运动模糊，看不出补帧伪影。

## Mixkit 与 Commons 补充实测（llm-launch-agate，2026-10-31）

- Mixkit 视频：同一类目里 Free 与 Restricted 混排，Restricted 的免费 720p 仅限个人使用（server 类 24 条全是 Restricted）；Free 视频最高 720p（1080p 返回 403）；约半数是竖屏。音乐列表在标签页 JSON-LD（`copyrightNotice`、`duration`、mp3 地址）；音效列表在页面的 `…/sfx/<id>/<id>-preview.mp3` 链接。
- Mixkit 许可（浏览器打开 license 模态框读取）：Stock Video Free 可商用、可广播；Stock Music Free 可用于网页 / 社媒 / 线上广告，不含 CD/DVD、电视与电台广播、游戏，不得 remix 成纯音乐或登记 Content ID；Sound Effects Free 含电视与电台广播，不得单独再分发。
- Commons：连续下载原图会被 429（返回提示改用标准缩略图），API `prop=imageinfo&iiprop=url&iiurlwidth=1920` 取 `thumburl` 可下；ffmpeg 对 `upload.wikimedia.org` 并发分段读同样 429，预览改为串行下载 480p 转码到本地再抽帧。
- Openverse 音频：6 组配乐检索词只得 Freesound 短音效，没有 ≥95 s 的完整曲目；6 次里 4 次网关超时。

## Pixabay 冒烟（2026-11-01）

- `pixabay-video "flooded street" --min-width 1920`：返回 10 条，库内共 500 条；多为 1920×1080，最高 2542×1440，时长 6–44 s，许可都是 Pixabay Content License，不要求署名。
- 相关度：前 3 条里有 2 条是水淹街道，其中第 3 条带 `ai generated` 标签；其余 7 条只是“street”。Pixabay 按标签匹配，检索词宜收窄，比如写成 `flood street water`，并看标签过滤 AI 生成内容。
- 配额：响应头为 100 次/60 s，与文档一致。
- 下载：`download_url` 是 `cdn.pixabay.com` 直链，不带 key，HEAD 返回 200（video/mp4）；这一次没有下载进成片。

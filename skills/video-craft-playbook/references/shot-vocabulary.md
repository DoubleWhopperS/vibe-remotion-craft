# 外部镜头词汇索引：video-shotcraft

[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)（Apache-2.0）是一个 Remotion 镜头配方库：124 张卡、150 式，每张卡带意图、参数表（含调节手感）、已知坑和一份 30 fps / 1920×1080 的 demo 源码。本页只做索引，帮规划时按职能和能量找词；卡的正文、参数和代码不搬进手册。

- **状态**：外部，本机未验证（2026-11-01 收录）。用过一张卡后，在案例卡里写明卡名和效果，按 [writeback.md](writeback.md) 判断能否升级。
- **语境**：作者的判例全部来自 web / 桌面产品宣传片。卡的运动语法换题材可用；节奏、能量骨架和判例数字在别的片种上要重新验证。
- **能力归属**：它是 capability-atlas A1 Remotion 上的一组现成实现，不是独立能力；选不选 Remotion 仍按 [task-lenses.md](task-lenses.md) 决定。
- **动态样片**：<https://vincentwei1021.github.io/video-shotcraft/>，按卡名搜索。

## 怎么用

1. 规划时按下面的职能槽位或生成段的分类扫「一句话」和能量，挑候选。
2. 读卡全文：`references/shots/<分类>/<卡名>.md`。卡里标注的命门参数（作者写「不得降档」）照原值起步。
3. 按卡的「参考实现」读 demo 源码。demo 依赖 `demos/_fixtures/`（`Look.tsx` 8 套调色板与字号阶梯，`Polish.tsx` 7 条带语义名的缓动、`ramp`、`SpeedBlur`），copy 时一并带上；用到 `staticFile('textures/live/…')` 的要把 `demos/_textures/` 的同名截图带进 `public/`。
4. 只继承运动语法、节奏和时值配比；字体、配色、材质按目标片的设计 spec 重新蒙皮。demo 画面里的标志与文案是 video-shotcraft 自己的，换掉。
5. demo 在占位文案上调校，词数、项数、页面尺寸变了要重算 stagger 和落位（各卡「已知坑」写了怎么算）。
6. 本机没有克隆时：`git clone --depth 1 https://github.com/Vincentwei1021/video-shotcraft.git`。只读卡和源码，不必安装它的 Skill 与工作台。

## 职能槽位 → 卡例

槽位来自作者的全片骨架（下一节）。卡例只是每格里一眼能对上的几张，完整列表见生成段。

| 槽位 | 分类 | 卡例 |
|---|---|---|
| 品牌开场、字标显影 | opening | `brand-ink-open`、`letterspace-materialize`、`text-as-mask`、`fracture` |
| 单主角立传、点名特写 | opening / camera | `spotlight-hero-card`、`crash-zoom-punch`、`tension-camera-moves` |
| 界面批量登场 | ui-entrance | `deck-deal-flyin`、`card-stack`、`row-embed`、`list-stack-press`、`wall-reveal-moves` |
| 功能演示、交互 | interaction / camera | `type-and-filter`、`cursor-flyover`、`theme-switch-moves`、`graze-face-tour` |
| 呼吸字卡、标题 | typography | `paper-title-card`、`blur-slide`（低能量标题）、`pill-slot-cycle`、`typewriter-moves` |
| 数据与指标 | data | `chart-live-moves`、`gauge-readout-moves`、`scroll-brake-moves`、`before-after-slider-scrub` |
| 镜头接缝 | transition | `shot-transitions`（按能量落差与接缝语义分三式）、`transition-hidden-cut`、`circle-match-iris` |
| 节奏峰、速剪 | rhythm | `beat-cut-moves`、`trailer-grammar-moves`、`quad-split-parallel-scenes`、`speed-ramp-freeze` |
| 强调与光 | effects | `light-play-moves`、`fui-hud-moves`、`slam-entrance-moves` |
| 收场、字标落版 | outro | `outro-group-photo-launch`、`logo-shrink-wordmark-lockup`、`ui-strip-away-outro` |

外部视频素材（生成底片、实拍）要进这些卡时，仓库的 `assets/lib/ClipCard.tsx` 把 mp4 包成圆角卡，可直接被 `spotlight-hero-card`、`magician-card-flourish`、`neon-frame-orbit-drop`、`quad-split-parallel-scenes` 的运镜驱动，素材短于镜头时交叉淡化续播。

## 全片能量骨架（外部单例判例）

作者的 30–60 s 多功能 web 产品宣传片模板与两次独立复现都收敛到同一骨架（`references/sequences/promo-energy-arc.md`）。作者自己标注为单例判例；15 s 短片或单功能产品可以合并段位，两端的字标停留和收场峰值保留。

| 段位 | 时长占比 | 能量 | 职责 |
|---|---|---|---|
| 品牌开场 | 8–12% | 低 | 字标落定后停留 ≥1 s，交棒产品画面 |
| 单主角立传 | 12–15% | 中，质感最高、节奏最慢 | 一个主角走完一条 ≥3 s 的动作弧 |
| 功能爬升 | 55–65% | 中高与低交替 | 每镜绑一个功能，一种手法全片只当一次主角；每 1–2 镜插一张约 1.8 s 的呼吸字卡，全片 2–4 张；信息最密的文档类镜头排在收场前倒数第 2–3 位 |
| 收场 | 13–16% | 全片峰值 | 前面出现过的元素围住字标合影，落定停留 ≥1 s |

排时间线时每镜先划走停留帧（落定 ≥30 f、批量收尾约 15 f），再排动效；转场帧从相邻镜头的预算里扣。

## 卡片索引（生成段）

由 `scripts/shot_vocabulary.py <仓库路径>` 从仓库的 `gallery/api/library.json` 生成，手改会被覆盖。每类内按能量从高到低排；「式」列只在一张卡有多个变体时填数。

<!-- generated:start -->
来源：video-shotcraft `library.json` revision bdd94be16d60fa8f，仓库提交 1266a3e；124 卡 / 150 式；卡片最近更新 2026-10-02。


### opening · 开场与品牌（11 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `fracture` | 高 | 约 5.2s | 5×5 瓦片从 3D 碎片态按中心波纹逐圈聚合成整面海报，停一拍亮字 |  |
| `magician-card-flourish` | 高 | 156f | 午夜蓝暗场上蓝色星芒闪现 0.3s，卡片从闪光点弹射而出 |  |
| `crane-rise-reveal` | 中高 | 5.5s | 升降臂拉升揭示：开场怼在一行数据特写，相机沿 Y 轴减速升起后拉 |  |
| `text-as-mask` | 中高 | 165f | 文字视频遮罩：瓷白舞台上切出超粗大标题字，字内部透出缓慢平移的暗色实时产品面板 |  |
| `icon-field-colorize` | 中 | 浮现 ~45f 错峰 + 静置… | 灰阶小图标点阵错峰浮现铺满全屏，停一拍后多道品牌色横带波纹极快向下扫翻全场 |  |
| `orbit-ring-title-open` | 中 | 150f | 石墨暗场上八张 16:9 暗色内容卡按 45° 均布在 720×380 椭圆上匀速公转 |  |
| `spotlight-hero-card` | 中 | 172f | 关灯的剧场里一束钨丝聚光扫过页面锁定一张卡，斜侧推进后卡片弹起悬浮、香槟色光束沿轮廓两圈 |  |
| `stroke-segment-build` | 低起中收 | 165f | 断笔成字：标题拆成十几段互不相连的笔画乱序逐段点亮，前 70% 不可读 |  |
| `brand-ink-open` | 低 | 约 2.8s | 墨线十字准星描画→字标逐字压印→打字机副标→满一秒静止再上浮消散 |  |
| `dataviz-landscape-open` | 低开缓升 | 5–8s | 暗场支流线束地景开场：多条流线汇入主干、虚构 ID 标签浮在线上、相机重景深低速飞越 |  |
| `letterspace-materialize` | 低 | 静置 ~15f + 描画 ~5… | 大字距字标全字符并行连续描画结晶 |  |

### camera · 运镜与空间（10 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `crash-zoom-punch` | 高 | 约 0.5s 动作 + 前后 … | 全景一拍急推到目标特写，落位二选一 |  |
| `space-camera-moves` | 高 | A 170f；C 105f单向… | 3D 空间化运镜两式：exploded-view 爆炸分解 | 2 |
| `tension-camera-moves` | A高/B低收 | 单式 5–6s；全片合计 ≤2… | 情绪运镜两式：bullet-time 冻结环绕、pull-back 拉远孤立 | 2 |
| `graze-face-tour` | 中高 | 单段 4–5s；可多段接力延长 | 大倾角贴面游走特写：镜头贴着 UI 表面低飞掠过，页面文字初始悬浮在界面上空带同形软影 |  |
| `steep-tilt-glide` | 中高 | 4s单镜；页面越宽越可拉长 | 固定镜头下直立页面以 60° 强透视侧立，页面自身沿其 3D 横面方向滑移掠过镜头 |  |
| `basic-3d-scene` | 中 | 约 7.5s | impress.js 式空间演示：卡片以不同位置/旋转/缩放散布 3D 空间 |  |
| `cursor-flyover` | 中 | 约 8.0s | 整页俯瞰后，相机依次飞到四个功能区 zoom-in 特写，SVG 光标先一步到位指点 |  |
| `depth-layer-moves` | 中 | 4–5.5s 持续 | 分层深度运镜：多层视差滑轨：3 层速度梯度横移出纵深，滑轨落定时主角浮起 |  |
| `overhead-camera-moves` | A中/B中高 | A 120f/ B 140f | 俯拍揭示两式：tilt-reveal 俯仰抬正揭示 | 2 |
| `terminal-3d` | 中 | 约 8.2s | 三个终端窗散布 3D 空间，相机窗间飞行、途中正弦拉远，每到一窗打字机敲命令、结果逐行滑出 |  |

### transition · 转场（15 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `card-flock-tumble` | 极高 | 翻飞 ~1.5s + 慢转展示… | 三张 UI 页卡从侧棱薄边 3D 翻飞成阶梯站定，站定后保持慢转不停，快速收束吸入中心 |  |
| `tear-streak-transitions` | 高 | 前态 ≥40f + 撕裂 16… | 撕裂转场：glitch-displace 噪声撕裂，数字故障语义的条带级撕裂 |  |
| `card-flip-reveal` | 中高 | 全程 150f；单卡 4f 预… | 功能卡 3D 翻面揭示：卡片沿 Y 轴翻 180° |  |
| `circle-match-iris` | 中高 | 5.5s / 165f | 圆心匹配光圈切：光圈从页面上圆形元素的圆心炸开，圈内新页的圆形图表接在同一个圆上 |  |
| `page-turn-transitions` | 中高 | 单式 150f，约 5.0s | 整页体块转场：barn-door-split 对开门裂幕 |  |
| `white-flash-logo-simplify-cut` | 中高 | 约 4s | 液态金属质感的彩色词标静置流光，蓄力后从字心炸出一记白闪过曝 |  |
| `bottom-push-stack-wipe` | 中 | demo 三连推 170f | 底边上推换章：新场景连底色整屏从底边向上推入，把旧场景物理顶出画外 |  |
| `line-carry-transition` | 中 | ~6.3s / 190f | 线条接力横移转场：场景 A 的进度条延伸出画，镜头跟线横移 |  |
| `mosaic-reframe` | 中 | 约 7.1s | 12 张瓦片在规则网格、feature mosaic、对角瀑布串三种排版间连续变形 |  |
| `print-texture-transitions` | 中 | 4–4.5s | 印刷质感转场：ink-bleed-reveal 墨渗揭示 |  |
| `shot-transitions` | n/a | n/a | 镜头交棒三式：推进流白、whip-pan 甩镜、mask-wipe 穿窗 | 3 |
| `transition-hidden-cut` | n/a | n/a | 藏切点转场三式：前景遮挡隐形切、对撞开屏、暖色漏光 | 3 |
| `transition-travel` | n/a | n/a | 穿越式转场：字腔穿越：巨型章节标题的字形就是一扇窗，镜头钻进字形笔画完成换景 |  |
| `wipe-transitions` | 中 | 前态 ≥20f + 擦除 ~5… | 几何擦除转场：blinds-slice 百叶窗切条 |  |
| `gradient-transition` | 低 | 约 6.7s | 背景在 linear、radial、conic 三类 CSS 渐变间平滑过渡 |  |

### typography · 文字与字卡（22 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `countdown-arc-scatter` | 高 | 约 3.3s | 纸面表盘 9 个等大数字沿大弧切向排布，整盘扫过 96° 后减速急停 |  |
| `flying-words` | 高 | 约 6.0s | 22 个关键词按黄金角铺在扁椭圆截面上，沿 z 轴从远处飞到相机前擦身而过 |  |
| `gradient-word-sweep` | 高 | 扫充 ~15–20f+ 稳态闪… | 黑底标语里关键词被渐变彩光从左到右快速扫过"充能" |  |
| `outline-word-fill` | 高 | 约 3.0s | 空心词从 3.2 倍急缓收缩落位，虚线大圆随后从 2.8 倍收到字周围并缓慢自转 |  |
| `type-rhythm-sync` | A高/B中 | A FontWeightPum… | 文字随声同步两式：font-weight-pump 字重脉冲与 karaoke-fill-… | 2 |
| `glitch-cycle` | 中高 | 约 5.6s | 同一行等宽槽位循环轮播 4 条状态短语，每条头尾按概率关键帧 [1,0,0,0.1,0,0… |  |
| `lead-word-zoom-assemble` | 中高 | 约 2.8s | 首词以 2.3 倍字号占据画面中央、hold 期间继续推近 6% |  |
| `type-entrance-moves` | 中高 | 单式 5s | 标题文字入场一式：letter-drop-physics 字符坠落 |  |
| `word-relay-geometry` | 中高 | 约 6.0s | 三个利益词各带一套专属几何接力 |  |
| `brace-expand` | 中 | 约 4s | 一对紧贴的小花括号先在正中出现，随即带一次过冲向左右弹开并放大到标题级 |  |
| `pill-chip-slot-cycle-handled` | 中 | 约 5.0s | 白底句式 "Your `chip` Handled" 里深色胶囊内词竖向滚轮轮换 |  |
| `pill-slot-cycle` | 中 | 入场 12f + 每拍 21f… | 句中词槽轮换：固定句干钉死不动，句尾 pill 徽章每 ~0.7s 老虎机滚一格 |  |
| `type-assembly-moves` | A中/B中高/C中 | 单式 4–5.5s | 文字集结三式：split-text-stagger 逐字裂升 | 3 |
| `vertical-word-roll-blur-cycle` | 中 | 约 5.0s | 句尾词换成竖向滚轮，3 次换词各 0.55s，相邻行按距离上垂直 blur 与灰度 |  |
| `document-typewriter-reveal` | 低中 | 150f | 悬浮在暗场里的整页真排版文档窗口在光标后自己"写"出来、侧栏跟进、历史条目逐个落入轨道 |  |
| `text-column-converge` | 中低 | 轮换 7–16f/词 × 8–… | 双词对峙合拢：左"NEW"右特性词钉死在等屏边距两侧硬切轮换、全程零收缩 |  |
| `title-demote-to-label` | 低中 | A ~3.7s/ B ~4.5… | 大标题降格为节标签两式：A 大标题居中显影站稳一拍后连续缩小 0.3x 平移到左上角落成小… |  |
| `typewriter-moves` | 中低 | ~5.3s | 打字机 error-retype |  |
| `word-relay-filmstrip` | 中低 | 每词期 ~1.5–2s × 3… | 左列黑白相间等高页面卡步进滚动、右侧衬线大词原位接力 |  |
| `blur-slide` | 低 | 约 4.0s | 标题逐词入场，y 0.38em→0 + blur 18→0 + opacity 0→1 三… |  |
| `marker-underline-title` | 低 | 标题落定 +4~8f 后起笔 | 大标题落定后，关键词下方马克笔下划线从左到右快速描画 |  |
| `paper-title-card` | 低 | 1.7–1.8s | 一句话逐词压印上纸、一个词标强调色斜体、短划线收束 |  |

### ui-entrance · 界面登场与陈列（21 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `deck-deal-flyin` | 高 | 150f | 暗色石墨桌面上的实体牌堆特写环绕开局，灯从牌堆亮到旁边的页面板 |  |
| `card-stack` | 中高 | 约 5.0s | 一组模板卡从屏幕下方逐张 spring 弹入、越落越快叠成一摞，全员落位后整摞一次性展成扇面 |  |
| `integration-hub-map` | 中高 | 前摇 ~0.5s + 快翻 ~… | 旧页面一次性快翻 180°落成新中枢页，五个集成 app 图标同帧弹现 |  |
| `neon-frame-forerun` | 中高 | 框奔画 ~0.7s + 点亮&… | 强透视直角霓虹框自左缘两头奔画先行成型，页面在框内由暗转亮 |  |
| `neon-frame-orbit-drop` | 中高 | 描框 ~0.5s + 旋转&同… | 霓虹框先行描框后，镜头绕页面左→右弧线旋转，页面全部组件/文字**同帧**从空中往下贴合 |  |
| `radial-wave` | 中高 | 约 3.8s | 17×9 圆点阵列按到波源的欧氏距离错峰点亮，每点 scale 过冲到 1.5 再落回常亮 |  |
| `research-card-stack-scroll` | 中高 | 约 4.8s | 深色论文卡每 12 帧一张沿右下轴线飞入中心叠压，落位带 1 帧压缩 |  |
| `value-stagger-gradient` | 中高 | 约 5.0s | 16 根柱入场时 delay 是时间错峰，同时高度/色相/位移/模糊四个属性各自铺成从首到… |  |
| `avatar-bracket-carousel` | 中 | 约 5.2s | "Your ___ agent" 填空排版，四角对焦框钉在句中不动 |  |
| `bezier-source-converge-merge` | 中 | 约 5.6s | 左侧四个来源节点各有一条细贝塞尔曲线连向右侧同一汇聚点，曲线先错峰由左向右 draw-on |  |
| `carousel-3d` | 中 | 约 5.6s | 8 张卡排成圆环整环自转一圈，每卡只绕 Y 公转、自身 billboard 朝外 |  |
| `cloner-depth-echo` | 中 | 138f | 克隆纵队：主卡瞬间"复印"出 7 个半透明分身沿斜向纵深排开成队 |  |
| `draw-svg-trace` | 中 | 132f | 描边生长圈注：一条带笔头的墨线沿元素轮廓跑一圈把它"画"出来，闭合瞬间闪黑交棒、内容淡入 |  |
| `list-stack-press` | 中 | 约 3s | 列表卡从画面底部逐张飞上摞起，每张落地压弹整摞、计数器同步跳一格 |  |
| `page-waterfall-wall` | 中 | 4–6s | 页面瀑布墙：真实页面截图切成 3–4 列在 3D 后仰墙面上差速反向无限滚动 |  |
| `product-card-progressive-assemble` | 中 | 约 5.7s | 详情卡像被逐字段抓取般自建：一枚"填充光标"领先跳格 |  |
| `row-embed` | 中 | 约 2s | 内容行像卡片一样从空中降下、rotateX 收平、嵌入瞬间底边亮一道强调色的缝 |  |
| `wall-reveal-moves` | 中 | 单式约 5s | 整墙批量入场两式：bento 逐格点亮、蓝图描线成形，全部原位显形不位移 | 2 |
| `element-body-moves` | A低中 | A 150f 5s | 元素身体感：contact-shadow-lift 接触阴影离面抬升：卡抬起时桌上的阴影同… |  |
| `doc-park-left-pill-deal` | 低 | 约 5.8s | 文档不淡出而是向左滑出只露约 35% 宽并微缩到 0.92 |  |
| `list-reveal` | 低 | 约 4s | 垂直菜单 6 项按 10f 的间隔依次 scale 找位、软 back 轻微过冲落定 |  |

### interaction · 交互与功能演示（11 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `autolayout-gap-dial` | 中 | ~5s | 间距拨盘驱动布局：一排链接块带框选描边+缝隙间距标注，徽章数字逐格跳动 |  |
| `canvas-materialize-moves` | 中 | A ~5s/ B ~6s | 内容"物化上画布"两式：panel-to-canvas 行倒卡与 diagram-casc… | 2 |
| `hashtag-to-pill-materialize` | 中 | 120f——打字 ~40f +… | 话题词打字实体化：居中打出 "#word"，1 帧硬切变成宽大胶囊标签 |  |
| `picker-carousel-feature-cycle` | 中 | 约3.6s | 移动端风竖向选择器：焦点药丸不动、内容穿过它，每项带明显 outQuint 减速吸附后完全… |  |
| `segmented-thumb-hero` | 中 | ~3.5s | 分段控件 thumb 位移当主角特写 |  |
| `theme-switch-moves` | A中/B中高 | A 140f/ B 156f | 主题切换两式：theme-sweep 斜向扫场与 palette-ripple 组合款 | 2 |
| `type-and-filter` | 中 | 约 2.5s | 真实 UI 上打字搜索、网格自己收敛成一张卡、点击穿透进详情页 |  |
| `voice-waveform-live` | 中 | 172f | 录音胶囊实时声纹：64 根细竖条随"说话"起伏，说话时中部高耸、停顿缩成点线 |  |
| `chip-grid-single-select-blackout` | 中低 | 约5.5s | 五个选项 chip 以 3+2 居中排布逐个淡入；选中帧先插一帧灰色按压块 |  |
| `collab-cursor-moves` | A低中 | A ~5.2s | 协作光标当演员：cast-ensemble 五光标群演氛围层 |  |
| `glass-pill-dictation-typing` | 低 | 约3.3s | 一条定宽玻璃胶囊以约 1.25 倍略大弹出后缓落到位，内部自左淡到右浓铺一层强调色暖光 |  |

### data · 数据与指标（5 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `chart-live-moves` | 中高 | 各 165–192f | 活体图表三式：oscilloscope-stream 示波流线 | 3 |
| `gauge-readout-moves` | 中高 | A 140f/ B 150f | 仪表读数两式：needle-sweep-selftest 满弧扫针与 tape-scrol… | 2 |
| `scroll-brake-moves` | 高开中收 | A 4–5s / B 5s | 长卷急刹两式：changelog-scroll-brake 基本款与 brake-reti… | 2 |
| `timeline-travel` | 中高 | 4–5s | 时间轴横移：镜头沿水平刻度轴加速掠过版本刻度，每过一格卡片弹立短停，末刻度急停推近 |  |
| `before-after-slider-scrub` | 中 | 4–5s | 前后对比拉杆："处理前/后"两版叠放，分割杆先猛甩后慢扫，杆过处新版"显影"揭出 |  |

### effects · 光效与强调（15 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `impact-feedback` | 高 | n/a | 命中反馈两式：hit-counter 连招计数、anime-impact 动漫打击帧 | 2 |
| `riso-print-hits` | 高 | 4s | 套印错位冲击帧：riso-misregistration-hit 单发：标题撞停瞬间裂成双… |  |
| `slam-entrance-moves` | 高 | 单式动作段 6–22f + 冲… | 高能砸入三式：kanada-perspective-snap 金田透视急停 | 3 |
| `assemble-then-type-flyin` | 中高 | 约5.6s | 空的暗底网格上，无文字的组件骨架先从四面八方飞入贴合 |  |
| `fui-hud-moves` | 中高 | 2–3s | FUI/HUD 准星咬合：reticle-lock-on 四个 L 形角标组成的取景框从画… |  |
| `scanline-assemble-flyin` | 中高 | 约5.2s | 页面开场是一张只有网格与虚线槽位的蓝图画板，一条亮扫描线自上而下掠过；扫到每个槽位 |  |
| `aurora-bloom-bg-flip` | 由低到高 | 约5.2s | 浅灰底从底部升起紫橙柔焦 blob，随后整个底色在约 0.36s 内压暗到近黑 |  |
| `brand-frame-snap` | 中 | 单次翻色 ~4.7s | 品牌色画框语法：一圈粗纯色画框先于内容长出包住全屏，录屏窗口落进框内 |  |
| `icon-performance-moves` | 蓄势引入 | 156f | 图标表演：attention-bounce 求关注弹跳 |  |
| `light-play-moves` | A中/B低 | A 170f ~5.7s / … | 光效两式：spotlight-sweep 聚光扫字、sheen 单点扫光 | 2 |
| `scanline-annotate-focus` | 中 | 约5s | 一条扫描线自上而下匀速掠过已存在的页面，越过哪块区块的下缘 |  |
| `scan-bracket-sweep` | 中低 | 约5.0s | 文档弹到中央，四角落下 L 形取景括号，一条扫描光带拖着渐变尾迹在文档上往复扫 5 趟 |  |
| `spotlight-sweep-moves` | 中低 | 单式 3.5–4.5s | 暗场聚光显影三式：A 醒睡扫过、B 贴边泛光横摇、C 角落匀速显影 | 3 |
| `glow-flyline-moves` | A低/B中/C中高 | A 170f/ B 140f/… | 暗场光斑与飞线三式：glow-orb-ambient 光斑底噪 | 3 |
| `radial-ripple-phone-chips` | 低 | 约5.6s | 暖沙底四层同心圆错相呼吸如水波，中央手机 mockup 屏内 feed 自动缓滚 |  |

### rhythm · 节奏与蒙太奇（8 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `beat-cut-moves` | 高 | 全程 140f ≈4.7s | 硬切当节拍乐器：连闪定格：三次白闪各硬切同一画面的一个裁切，快门余韵沉降后停在特写收束 |  |
| `beat-step-list-theme-cycle` | 高 | 铺垫 30f + 每拍 18f… | 三通道节拍器：深色场形容词列表逐拍上移一行，视口中央固定胶囊"接住"下一个词并换色 |  |
| `quad-split-parallel-scenes` | 高 | 90f | 画面硬切 2×2 四宫格，四个象限并行跑各自的微场景，关键节拍错开 3–6 帧制造信息轰炸 |  |
| `trailer-grammar-moves` | A高 | A ~4.7s | 预告片语法一式：trailer-bumper 前置速剪钩子：三镜 9f 速剪 + 黑场静默… |  |
| `panel-grid-moves` | 中高 | 156f ≈5.2s | 分格节奏：comic-panel-split 漫画斜格劈出同一主体的三个机位 |  |
| `sakuga-timing-shift` | 中高 | 150f | 一拍三转一拍一：元素先以每 3 帧一步的手翻书顿挫移动，高潮瞬间切成逐帧丝滑冲刺 |  |
| `speed-ramp-freeze` | 中高 | 定格标注全程 158f | 帧号非线性 remap 的节奏手法 |  |
| `rhythm-interrupt-moves` | A中 | A 135f ≈4.5s | 打断节奏：jump-cut-punch-in 三级跳切推近：同构图三次无补间硬跳放大 |  |

### outro · 收尾（6 卡）

| 卡名 | 能量 | 时长 | 一句话 | 式 |
|---|---|---|---|---|
| `outro-group-photo-launch` | 峰值 | 约 4.8s | 全片元素从四面八方飞来围住字标合影，crane 落机位+舞台光+金尘做成发布会收场 |  |
| `grain-dissolve` | 中高 | 约 2.0s | 整行字爆裂成沸腾颗粒噪点并浮现斜纹选区框，噪点云急速凝聚成更大号发光短字标，位移衰减归零定格 |  |
| `neon-triple-marquee` | 中高 | 4–5s | 三行对向霓虹跑马灯 recap |  |
| `ui-to-brand-morph` | 中高 | A ~4.3s/ B ~5.6s | UI 变品牌两式：icon-flip-bloom 图标 Y 轴翻扁成竖线 | 2 |
| `logo-shrink-wordmark-lockup` | 中 | 约 4.4s | 霓虹切口大环快速收束成中央实心小白 O、过冲刹车时换成 video-shotcraft 标… |  |
| `ui-strip-away-outro` | 中 | ~4.8s | 减法式收尾：点击 Publish 后整个编辑器 UI 从外围到中心层层错峰蒸发 |  |
<!-- generated:end -->

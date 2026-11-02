# 能力地图

每张卡描述一种可调用的能力：它产出什么、在什么表达上成立、边界在哪、确定性与代价、能和谁拼接、从哪里调用、验证到什么程度。卡片按媒介类别排列，顺序不代表排名。

验证状态分三级：
- **案例验证**：在本机成片案例里用过，写明项目（项目在 `$MG_WORKSPACE/projects/`）。
- **已安装未验证**：本机可调用，但还没进过成片。
- **推断**：依据文档或经验判断，未实测。其中“文档核实”指已对照官方当前文档确认 API 存在与用法，仍未实测。

具体模型清单、版本、单价变化快，卡里只写到能力层；调用前以对应 Skill 或平台的当前清单为准。

卡片字段定长（`check` 校验，单字段超 400 字符 warn、超 600 FAIL）：“擅长的表达”写表达类别，不写功能清单；文档能查到的 API、参数、版本行为只留指针；具体实现去向工作区技法表。

## 总览

先扫这张表挑出候选，再读对应卡片；顺序按媒介类别，不代表排名。

| 编号 | 能力 | 产出 | 确定性 | 代价 | 验证 |
|---|---|---|---|---|---|
| A1 | Remotion | React 按帧渲染；DOM / SVG / Canvas2D / WebGL / three.js 同工程 | 高 | 免费 | 案例验证 |
| A2 | HyperFrames | 模型写 HTML 动效渲成视频 | 高 | 免费 | 案例验证 |
| A3 | Python 逐帧管道 | numpy / PIL 逐帧 → ffmpeg | 高 | 免费 | 案例验证 |
| A4 | 浏览器录屏 | Playwright / CDP 录真实网页 | 中 | 免费 | 案例验证 |
| A5 | anatomy 等距交互图 | 等距 SVG 交互页，经录屏成视频 | 高 | 免费 | 案例验证 |
| B1 | three.js / R3F | 实时光栅化 3D | 高 | 免费 | 案例验证 |
| B2 | Blender | bpy 建模布光，EEVEE / Cycles 渲染 | 高 | 免费，渲染耗时 | 案例验证 |
| B3 | 物理引擎（离线烘焙） | 刚体模拟烘焙成位姿与接触事件 | 高 | 免费，调参耗时 | 案例验证 |
| C1 | 生成视频 | 文 / 图 / 参考生视频片段 | 低 | 付费 | 案例验证 |
| C2 | 生成图像 | 关键帧、底图、设定图 | 低到中 | 付费 | 案例验证 |
| C3 | 生成 3D 资产 | 图生网格，可绑骨 | 低 | 付费 | 案例验证 |
| C4 | Higgsfield 预设与工作流 | 平台封装的整条流程 | 低到中 | 付费 | 案例验证（Katana） |
| C5 | 旁白 / TTS | 按句生成语音 | 中 | 低；`say` 免费 | 案例验证 |
| C6 | 生成音乐 | 按情绪生成整曲 | 低 | 付费 | 案例验证 |
| C7 | 画布与编排平台 | 平台画布编排生成节点 | 低 | 按平台计费 | 已安装未验证 |
| D1 | ffmpeg | 剪辑、滤镜、混流、编码 | 高 | 免费 | 案例验证 |
| D2 | 离线逐帧合成 | numpy / PIL 在底片上抠像叠层 | 高 | 免费 | 案例验证 |
| D3 | 抠像与 matte | 前景 alpha | 中到高 | 阈值免费；平台付费 | 案例验证 |
| D4 | 超分与视频增强 | 分辨率与画质提升 | 中 | 付费 | 案例验证（fast 档） |
| D5 | 补帧与变速 | 时间重映射与中间帧 | 高；学习型中到高 | 免费 | 案例验证 |
| D6 | 视频稳定 | 去晃动与变换数据 | 高 | 免费 | 案例验证 |
| D7 | 调色匹配与统一 look | 镜头间统一与风格 LUT | 高 | 免费 | 案例验证 |
| E1 | numpy 音频合成与混音 | 配乐部件、拟音、总线混音 | 高 | 免费 | 案例验证 |
| F1 | 叙事与提示词 Skills | 剧本、分镜、prompt | 不适用 | 免费；出分镜图付费 | 部分验证 |
| G1 | 参考片拆解 | 切点、段落、声音结构 | 高 | 免费 | 案例验证 |
| G2 | 内容理解与语音识别 | 带时间戳转写、内容理解 | 中 | 低 | 案例验证 |
| G3 | 机器验收脚本 | 通过 / 失败信号 | 高 | 免费 | 案例验证 |
| G4 | 同步歌词数据源（LRC） | 行级时间戳歌词 | 中 | 免费 | 案例验证 |
| G5 | 镜头、主体与运动分析 | 镜头边界、质量分、轨迹、光流 | 统计高；模型中 | 本地免费 | numpy 路线案例验证 |
| H1 | 开放素材库检索与下载 | 实拍视频、照片、音效，附来源与许可记录 | 中 | 免费 | 案例验证（Commons 视频与图像、Mixkit；Openverse 已冒烟；Pixabay、Freesound 已冒烟；Pexels 停发新 key） |
| H2 | 本地素材库索引与检索 | 自有素材的镜头边界、标签、质量分索引 | 中 | 免费 | 推断 |

---

## A. 程序化画面（代码直接画出每一帧）

### A1 Remotion
- **产出**：React 组件按帧号渲染成视频；同一工程里可用 DOM/CSS、SVG、Canvas2D、WebGL、three.js（`@remotion/three`）。
- **擅长的表达**：排版与动态文字、UI / 产品界面重建、数据驱动的图形、旁白驱动的叙事 MG、2.5D 轴测、程序化笔触；DOM 底下垫全屏 WebGL 着色器补有机氛围、单张 Canvas2D 做光照合成、SVG 滤镜做墨迹洇开（实现见工作区技法表）；对素材做后处理：`@remotion/effects`（≥4.0.464）约 60 个着色器效果（模糊、色彩与 LUT、风格化、几何、色键，`createEffect()` 可自定义）、`@remotion/transitions` 的几何与着色器转场、`@remotion/motion-blur`、`@remotion/captions`，清单以官方文档为准；适合任意一帧可单独渲染、卡点精确、反复修改的片子。
- **边界**：没有真实的身体动作和实拍质感；光照受浏览器光栅化限制（无 GI、无景深）；跨帧状态在并发渲染下出错；长片 DOM 渲染偶有崩溃，需分段可续跑；跟踪、稳定、抠像、补帧这类要分析素材像素的工作由外部算好再交回数据或 alpha。着色器效果与转场要 `--gl=angle`（无 GPU 时 `swangle`）；HTML-in-canvas 类转场（filmBurn、zoomBlur 等）的 Studio 预览需 Chrome ≥149 开 `canvas-draw-element`，API 尚不稳定；`<CameraMotionBlur>` 损伤色彩、耗时随 samples 成倍增加（文档核实）；`lut()` 渲染后 ΔE 比离线高约 1.2（code-to-cinema）。
- **确定性**：高。画面是帧号的纯函数，随机数带种子即可完全复现。
- **代价**：免费；1080p 全片渲染从十几秒（three.js 短片）到约 4 分钟（236 s DOM + SVG 滤镜 + 全屏着色器，并发 6）不等，75 s 后处理片 2250 帧约 5 分钟（并发 4）；前期要写代码，后续每轮修改便宜。
- **接口**：输入图片、视频底片、音频、JSON 时间轴；输出 mp4 或 PNG 序列（可带 alpha）。可与生成底片、Blender 渲染序列、numpy 音频拼接。
- **入口**：`remotion-best-practices` Skill；本机模板 `$MG_WORKSPACE/template/remotion-starter/`（Remotion 4.0.536）；外部镜头配方库 video-shotcraft 的索引见 [shot-vocabulary.md](shot-vocabulary.md)（外部，本机未验证）。
- **验证**：案例验证（12 例，最近 code-to-cinema：18 种 effects、7 种着色器转场、`<Trail>`、captions 进成片；`<CameraMotionBlur>` 仍为文档核实）；核验 2026-10-24。

### A2 HyperFrames
- **产出**：由模型写 HTML（GSAP、Lottie、Three.js、CSS 动画、WAAPI 等运行时），渲染成视频。
- **擅长的表达**：HTML/CSS 动效、动态排版、短时长 motion graphic、logo 演绎、UI 动画、数据图表动画。
- **边界**：已做过 4 s logo 演绎（GSAP 时间线，渲成 mp4 交给 Remotion 叠效果，code-to-cinema）；复杂 3D、长叙事、逐像素合成没验证（外部 OpenDesign Motion 用它渲出 5 支 14–20 s 成片，含剪纸角色故事与 three.js 3D 字，本机未复现）。`lint` 禁止 tween letterSpacing 这类会按整数像素跳的属性（`gsap_non_transform_motion`），lint 报错时 layout / contrast 审查不会运行。
- **确定性**：高（框架要求单一暂停时间轴、可 seek）。
- **代价**：免费；需 `npx` 拉取指定版本。
- **接口**：HTML 合成；输出 mp4 或透明叠层。
- **入口**：`hyperframes-core`、`hyperframes-animation`、`hyperframes-keyframes`、`motion-graphics` Skill；`npx -y hyperframes@0.8.173`，运行前设 `HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_TELEMETRY=1`，不要运行 `hyperframes usage`（会读取登录凭据）。
- **验证**：案例验证（code-to-cinema 标题：`check` 0 错误、63/63 对比度通过，4 s 渲染 34 s）；核验 2026-10-24。

### A3 Python 逐帧管道（numpy / PIL → ffmpeg rawvideo）
- **产出**：Python 逐帧画出 RGB 数组，经管道交给 ffmpeg 编码。
- **擅长的表达**：几何变形、字体动画、解析曲面的光栅化（如金属环雕塑）；高帧率（60 fps）；需要逐像素控制、不想依赖浏览器的场合。
- **边界**：没有现成的排版、布局和 3D 管线，复杂场景要自己写；性能取决于向量化程度。
- **确定性**：高。
- **代价**：免费；开发成本集中在绘制代码。
- **接口**：输出 mp4；也常用来离线处理生成底片（见 D2）。
- **入口**：本机 `effects/snippets/numpy-frame-pipeline/render.py`（含 `--preview`、`--contact`、`--poster`）。
- **验证**：案例验证（make-it-move，15 s 1080p60）；核验 2026-10-23。

### A4 浏览器录屏
- **产出**：用 Playwright 等自动化工具操作真实网页并录屏。
- **擅长的表达**：快速出一版真实产品操作录像，零重建成本。
- **边界**：节奏、特写、画质不可控，难以卡音乐和做镜头推拉。
- **确定性**：中（依赖页面实时状态）。
- **代价**：免费。
- **接口**：输出视频，可作为合成底片。
- **入口**：Playwright；内置浏览器或 Chrome（web-access）用于先跑通 demo、量元素坐标。实时录屏：工作区 `effects/snippets/browser-record/record_cdp.mjs`（系统 Chrome + CDP `Page.startScreencast`，帧按时间戳排序后 ffconcat）；Playwright `recordVideo` 要另下载它自带的 ffmpeg。
- **验证**：案例验证（code-to-cinema：anatomy 页面 9 s 录到 536 帧，59.8 fps 实时；saas-launch 两个案例选了 DOM 重建）；核验 2026-10-24。

### A5 anatomy 等距交互图
- **产出**：带精细零件、四档明暗、缓动动画的等距 SVG 交互图（HTML 页面），可加 WebGL 着色器。
- **擅长的表达**：把一个技术概念讲成一台真实的仪器或机器。
- **边界**：产物是交互网页，不是视频；经 A4 实时录屏转成视频已验证（code-to-cinema，录屏时间不受合成端控制），改写成帧驱动没验证。暗色主题贴在暗背景上对比度低，合成端要提亮（`levels()`）。
- **确定性**：高（几何预计算、可审计）。
- **代价**：免费；一张 Figure 级图约 1 小时，Hero 级 2–4 小时。
- **接口**：独立 HTML / SVG。
- **入口**：`anatomy` Skill。
- **验证**：案例验证（code-to-cinema：Figure 档约 55 个零件的剪辑台进了成片，未跑 lines / 4× 验收）；交互图案例 `effects/interactive/anatomy-diffusion/`；核验 2026-10-24。

---

## B. 程序化 3D

### B1 three.js / React Three Fiber
- **产出**：实时光栅化 3D：透视或正交相机、自定义着色器、InstancedMesh、MRT 多通道。
- **擅长的表达**：体素与像素物件、等轴建筑（正交 + 按法线分档着色 + 深度/法线描线）、物理烘焙数据回放、渲染通道显形（热图 → 深度 → 成品）。
- **边界**：没有 GI 和真实软阴影，“棚拍质感”“草地、云海、落日”这类靠光照成立的画面难做；颜色管理要手动关（像素风）；r186 有若干 API 变化（见 pitfalls）。
- **确定性**：高。
- **代价**：免费；843 帧 1080p60 约 18–24 s（并发 4）。
- **接口**：在 Remotion 里用 `<ThreeCanvas>`，或独立页面；可读 Blender 导出的 `.glb`（节点名会被改写，序号放 extras）。
- **入口**：项目内 `npm install --save-exact three@0.186.1 @types/three@0.186.0 @react-three/fiber@9.8.2 @remotion/three@4.0.536`（已验证组合）。
- **验证**：案例验证（bell-machine、library-3d、city-love）；核验 2026-10-23。

### B2 Blender
- **产出**：Python（bpy）脚本建模、布光、动画，EEVEE 或 Cycles 后台渲染；也可经 MCP 操作正在运行的 Blender。
- **擅长的表达**：靠光照成立的质感（GI、AgX、接触阴影、空气透视）、粒子毛发的草地、云海、落日；带骨骼动画的角色；需要交给用户的 `.blend` 模型；作为“体量唯一权威”导出 `.glb` 和部件清单给其他渲染端。
- **边界**：Cycles 1080p 一帧 3–7.5 分钟（带草），只适合关键帧；EEVEE 1080p 48 采样约 6–11 s / 帧；生成资产的写实材质偏塑料感；EEVEE 与 Cycles 切换后部分材质表现不同；EEVEE 后台渲染要逐帧 `write_still`（`animation=True` 只出第一帧），面积光 20 盏以上会撑爆 shadow buffer 导致零阴影。
- **确定性**：高（脚本化场景 + 固定种子）。
- **代价**：免费；渲染耗时是主要成本，增量重渲可省大半。
- **接口**：输入 `.fbx`/`.glb` 资产、Tripo 角色；输出 PNG 序列 / mp4 / `.blend` / `.glb`；带锁定机位的灰盒 playblast 可作 C1 的参考视频输入（布局与运动归 playblast，外观归生成模型）。
- **入口**：`blender -b`（Blender 5.2.1，引擎名 `BLENDER_EEVEE`）；`blender-official` MCP（需 Blender 开着并启用插件）；本机脚本 `effects/snippets/ai3d-pipeline/`、`effects/snippets/iso-three/blender_boxes.py`；专家 skill 族 `scenario-blender-expert`（闸门 `bx_audit.deliverable`、审图 `bx_review`）+ blockout / previs-storyboard / lighting-rendering / animation / export，按 Scenario 插件工具名写，本机用 `execute_blender_code`；其导入函数会清空场景，只在后台跑。
- **验证**：案例验证（b612-slice 成片、library-3d 建模）；核验 2026-10-23。专家 skill（scenario-labs/skills@5429dea）2026-10-24 本机后台冒烟通过（9 个模块导入、闸门抓出悬浮件与未应用缩放、审图出图），未进成片。

### B3 物理引擎（离线烘焙）
- **产出**：真实刚体模拟，烘焙成逐帧位姿与接触事件，渲染端只读。
- **擅长的表达**：“过程本身成立”的片子：连锁机关、多米诺、碰撞卡点；接触事件同时驱动音效。
- **边界**：调参复杂（因果链逐环求解、分段与整段结果有数值串扰）；本机只验证了 2D 引擎 planck.js，3D 物理（Blender 刚体等）未试。
- **确定性**：高（烘焙后），并可用核验脚本证明全程只有一次外力。
- **代价**：免费；调参是主要时间成本。
- **接口**：输出 `sim.json`（位姿、接触、滚动状态），three.js 或任意渲染端回放。
- **入口**：本机 `effects/snippets/physics-sync/`（machine / tune / bake / verify）。
- **验证**：案例验证（bell-machine，38 次撞击卡鼓点 ≤2.5 ms）；核验 2026-10-23。

---

## C. 生成式模型（付费调用一律先报价、经用户确认）

### C1 生成视频
- **产出**：文生视频、图生视频、参考视频 / 多参考生成的视频片段（常见 5–10 s，24 fps）。
- **擅长的表达**：代码做不出的东西：真人与身体动作、手势、手持镜头与三维视差、鱼眼与运动模糊等镜头语言、有机纹理（墨迹扩散、烟、水）、实拍质感。生成的片段常当作“底片”或“素材库”交给合成端切用。
- **边界**：动作描述不一定被执行（“捏住再打响指”出成 OK 手势），精确时机要靠后期变速；清晰静止的手指是主要风险；真人输入视频会被拒；姿势描述可能触发审核（提交后约 20 s 失败退款且无原因）；文字和图形不要交给生成端；Seedance 2.5 的 t2v 不接受 `camera_fixed`，机位固定要写进 prompt；`generate_audio` 默认 true，静默素材也会因输出音轨被判版权失败。
- **确定性**：低。同一 prompt 结果不同，按“生成后先审片再用”规划。
- **代价**：付费。案例实测：按秒或按条计费，各平台单价差异大；有的平台没有提交前报价接口（只能用历史任务折算），Higgsfield 有 `get_cost`。
- **接口**：输入参考图（身份、场景各管一件事）、首尾帧、参考视频；输出 mp4，需映射到合成端帧率。首尾帧给同一张设定稿、prompt 写机位完全固定并逐条列“画里什么动、怎么动”，画内元素动起来又回到原构图，片段首尾能无缝接转场；5 s 里挑最好的约 1 s 再变速（外部 huashu-art-motion 路线 C，本机未验证）。
- **入口**：`tams-model-router`（Seedance、Kling、Wan、Vidu、Hailuo 等，以其当前清单为准）、`higgsfield-generate`；提示词前期见 F1。
- **验证**：案例验证（Seedance 2.5：katana-face-edit-2、fw26-lookbook、city-love）；其他模型已接入未在成片中验证；核验 2026-10-23。

### C2 生成图像
- **产出**：关键帧、场景底图、角色与道具设定图、风格帧、四视图。
- **擅长的表达**：给后续步骤当“规格”：空地底图直接做背景、同机位落成图用于标定投影和反算体量、角色设定图喂给 3D 生成、首帧喂给图生视频。
- **边界**：AI 轴测图常带透视（同方向边 20°–43°）；爆炸图部件常不守恒；场景底图模型会把参考帧里的人物照抄进“无人”底图；生长过程图不如代码推出的一致。
- **确定性**：低到中；每张先给用户确认再往下游走。
- **代价**：付费，单张便宜；返工发生在下游时代价放大。
- **接口**：输出 PNG，交给合成端、3D 生成或视频生成。
- **入口**：`gpt-image-2-prompt-enhancer`（GPT Image 2 提示词）、`higgsfield-generate`（含 Soul Cinema）、`tams-model-router`、`storyboard-generator`（分镜图）。
- **验证**：案例验证（arc-axo 关键帧作底图、fw26-lookbook Soul Cinema 底图、b612-slice 设定图）；核验 2026-10-23。

### C3 生成 3D 资产
- **产出**：图生 3D 网格（GLB/FBX），可选四边面、自动绑骨、预设动作重定向。
- **擅长的表达**：会走动的风格化角色（中景走路、站立）；树、石、花这类有机道具（一个母型复制多份）。
- **边界**：手指粘连；预设动作名不可信（`turn` 实为半蹲张臂）；无坐、蹲预设；四边面强制 FBX；写实 PBR 材质偏塑料；贴图带烘焙明暗。
- **确定性**：低；入库前要量化自审（面数、尺寸、姿势测试、动作抽帧）。
- **代价**：付费（Tripo：角色 120 + 绑骨 25 + 每个动作 10 credits，道具 40 credits，1 credit = $0.01；新 API 账号无免费额度）。
- **接口**：输出 FBX/GLB，交给 Blender 或 three.js。
- **入口**：`tripo` CLI 0.7.2（每条命令带 `TRIPO_ANALYTICS_ENABLED=0`，不运行 `tripo update`），预算拦截脚本 `effects/snippets/ai3d-pipeline/tripo_spend.sh`；Higgsfield `generate_3d`、`scene_builder_3d_*`（已接入未验证）。
- **验证**：案例验证（Tripo：b612-slice）；Higgsfield 3D 未验证；核验 2026-10-23。

### C4 Higgsfield 预设与工作流
- **产出**：平台封装的完整流程：Katana（实拍底片 + 图形叠加）、解说视频、Marketing Studio 广告、Shorts Studio 等。
- **擅长的表达**：实拍占大头、平台已有成熟模板的片子；快速出一版。
- **边界**：Katana run session 只有 1 小时；内置合成器装不下 three.js 等复杂图形；节奏和细节受模板约束。
- **确定性**：低到中。
- **代价**：付费，按预设计价。
- **接口**：输出 mp4；也可只借它的做法，把合成放到本地。
- **入口**：`higgsfield-generate`、`higgsfield-video-explainer` 等 `higgsfield-*` Skill（需用户明确选择 Higgsfield）。
- **验证**：案例验证（Katana：katana-face-edit-2、fw26-lookbook）；其他预设未验证；核验 2026-10-23。

### C5 旁白 / TTS
- **产出**：按句生成的语音。
- **擅长的表达**：中文旁白（百炼 qwen-audio-3.0-tts 系列，基础音色里有 6–10 岁童声，可用 `instruction` 描述语气）；英文旁白（ElevenLabs eleven_v3）；macOS `say` 本地免费，适合机器感的短句，逐词时刻可按逐前缀合成测出（code-to-cinema）。
- **边界**：同一句两次时长不同；只给整句对齐，逐词时刻要自己切；百炼句首单独的“AI”会读错；“句间自然停顿”指令会出长停顿或重复半句；ElevenLabs 没有童声，变调会有机械感。`say` 音质明显不如付费 TTS。
- **确定性**：中；每句生成后立即 ASR 核对。
- **代价**：低（百炼约 0.01 credit/字，0.2–0.8 credit/句）。
- **接口**：输出 wav；与时间轴、侧链混音配合。
- **入口**：`tams-model-router`（TTS provider）；本机 `effects/snippets/ai3d-pipeline/tts_qwen.py`、`projects/2026-10-23-saas-launch-v1/scripts/vo_prep.py`；`say` 版：工作区 `effects/snippets/voice-timeline/say_words.py`。
- **验证**：案例验证（city-love、b612-slice、saas-launch-v1、saas-launch-v2；`say` 在 code-to-cinema）；核验 2026-10-24。

### C6 生成音乐
- **产出**：按情绪描述生成的整曲（可纯音乐）。
- **擅长的表达**：有情绪描述、不需要严格按事件卡点的配乐（钢琴 + 八音盒 + 弦乐、发布会律动）。
- **边界**：BPM 不听 prompt（要 110 出 91.88），要先测节拍再排分镜；一次出约 2.5 分钟整曲，要自己截段落、做淡出；母带化的音乐叠音效瞬态时真峰值压力大。
- **确定性**：低。
- **代价**：付费（MiniMax music-2.6 按首计费）。
- **接口**：输出音频 URL；之后用节拍检测吸附画面段落。
- **入口**：`tams-model-router`（music provider）。
- **验证**：案例验证（b612-slice、saas-launch-v1、saas-launch-v2）；核验 2026-10-23。

### C7 画布与编排平台
- **产出**：在平台画布上编排图像、视频、素材节点。
- **擅长的表达**：多节点生成流程的可视化编排、团队共享（推断）。
- **边界**：本机未用于成片。
- **确定性**：低（生成为主）。
- **代价**：按平台计费。
- **接口**：平台 API / CLI。
- **入口**：`forge-canvas`、`libtv-cli` Skill。
- **验证**：已安装未验证；核验 2026-10-23。

---

## D. 合成与后期

### D1 ffmpeg
- **产出**：剪辑、滤镜、拼接、混流、响度测量与编码。
- **擅长的表达**：基于底片的推拉、遮罩、甩镜、划变、闪白闪黑、分屏、PNG 叠层、开场描边辉光（EDL 驱动）；所有路线最后的混流与交付测量。
- **边界**：不适合 3D 和逐帧图形；流拷贝拼接会留下不齐的时间戳；zsh 下拼参数有多处陷阱。
- **确定性**：高。
- **代价**：免费，快。
- **接口**：任意视频 / 音频 / 图片序列。
- **入口**：`ffmpeg-video-editor` Skill；本机 `effects/snippets/ffmpeg-edl-fx/cut.py`（EDL 剪辑器）、`effects/snippets/audio-sync/mux.sh`。
- **验证**：案例验证（fw26-lookbook 全片；所有项目的混流与响度测量）；核验 2026-10-23。

### D2 离线逐帧合成（numpy / PIL）
- **产出**：在生成底片上逐帧做抠像合成、调色、叠层。
- **擅长的表达**：文字放到人物身后、热成像色调、HUD、故障效果、墨团只在人物轮廓里发生；把一条生成素材拆成可复用的带 alpha 序列。
- **边界**：没有时间轴编辑界面，全靠脚本；生成底片 24 fps 要映射到成片帧率。
- **确定性**：高。
- **代价**：免费。
- **接口**：输入底片与 matte，输出 PNG 序列或 mp4，交给 Remotion / ffmpeg。
- **入口**：本机 `effects/snippets/overlay-compositing/fe2_comp.py`、`effects/snippets/thermal-plate/plates.py`。
- **验证**：案例验证（katana-face-edit-2、city-love）；核验 2026-10-23。

### D3 抠像与 matte
- **产出**：前景 alpha。
- **擅长的表达**：给合成端分层。若在生成阶段就把背景和光写成“能直接抠”的样子（过曝逆光窗户、纯黑背景、俯拍白纸），亮度阈值就是 matte，可省掉抠像模型。
- **边界**：`remove_background` 输出黑底人物、没有 alpha，要用 matte 与原片的比值重建；CSS `mask-image` 在 Remotion 里不会被等待加载；主体比背景暗时（墨、烟、剪影）亮度阈值出不了 matte，改用静止背景差分，毛边另拆 core / fringe。
- **确定性**：中到高。
- **代价**：亮度阈值免费；平台抠像付费。
- **接口**：输出 alpha 序列。
- **入口**：Higgsfield `remove_background`；D2 的脚本。
- **验证**：案例验证（katana-face-edit-2、city-love）；核验 2026-10-23。

### D4 超分与视频增强
- **产出**：分辨率提升、画质增强。
- **擅长的表达**：生成底片从 720p 提到交付规格。
- **边界**：生成式增强会改动细节；临时结果 URL 约 24 h 失效。
- **确定性**：中。
- **代价**：付费（MediaKit 720p/12 s：fast≈4、standard≈15、generative≈50、professional≈150 credits，1080p 翻倍；lensless 实测 fast 出 1080p：6 s 生成片 4.03、5 s 3.36 credits，帧数与 24 fps 不变）。
- **接口**：输入视频 URL，输出视频 URL。
- **入口**：`tams-model-router`（mediakit-video-enhancement）、Higgsfield `upscale_video`。
- **验证**：案例验证（lensless：4 条 Seedance 720p 底片经 fast 提到 1080p 进成片，并发约 2 分钟完成）；standard / generative / professional 仍只有工具实测（tams-model-router 2026-09-04）；核验 2026-10-30。

### D5 补帧与变速
- **产出**：时间重映射后的视频：分段恒速、连续速度曲线、定格、倒放，以及慢动作所需的中间帧与帧率转换。
- **擅长的表达**：把动作峰值对到节拍或事件点的变速坡道（editing-grammar EG-30）；动作高光的慢动作；生成底片 24 fps 转 30 / 60 fps；生成素材时机不受控时用变速对齐时间权威（craft-lessons L12）。
- **边界**：帧复制在慢动作下顿挫，帧混合出重影；光流补帧（ffmpeg `minterpolate`）和学习型补帧（RIFE 类）在遮挡、快速运动、细线和文字处出现扭曲与拖尾；连续速度曲线在 Remotion 里要自己把成片帧映射到源时间（推断）；变速后的原声需要单独处理（变调、静音或换音效）。
- **确定性**：帧复制、帧混合、光流补帧高；学习型补帧中到高（随模型与版本变化）。
- **代价**：ffmpeg 免费，`minterpolate` 很慢；学习型补帧本地需要 GPU 或付费平台（推断）。
- **接口**：输入源视频 + 时间映射表（成片时间 → 源时间）；输出视频或 PNG 序列交给合成端。
- **入口**：ffmpeg `setpts`、`framerate`、`minterpolate`（D1、`ffmpeg-video-editor`）；学习型补帧工具本机未安装。
- **验证**：案例验证（code-to-cinema：minterpolate mci 把 12 fps 36 帧补成 60 fps 171 帧，再按速度曲线取样做 0.25× 坡道，与重复帧版并排对照）；学习型补帧未验证；核验 2026-10-24。

### D6 视频稳定
- **产出**：去除意外晃动后的视频，以及每帧的变换数据。
- **擅长的表达**：手持实拍、晃动的录屏或生成片段在推镜、重构图、跟踪标注之前先稳定（editing-grammar EG-23）；变换数据也可以反过来加回去，做可控的手持感。
- **边界**：稳定要裁边或放大，损失分辨率；卷帘快门的果冻变形修不干净；画面稳了，原有的运动模糊还留着，看起来糊；刻意的手持感会被一起抹掉；大面积运动的主体会干扰估计。
- **确定性**：高（两遍分析算法，参数固定即可复现）。
- **代价**：免费。
- **接口**：视频 → 视频；`vidstabdetect` 输出 `.trf` 变换文件，可导出给其他宿主驱动变换。
- **入口**：ffmpeg `vidstabdetect` + `vidstabtransform`（两遍），或单遍 `deshake`（D1）。
- **验证**：案例验证（code-to-cinema：vidstab 两遍 smoothing 30 + zoom 6%，相位相关测相邻帧全局位移，抖动 3.61 → 0.71 px/帧 RMS）；核验 2026-10-24。

### D7 调色匹配与统一 look
- **产出**：镜头间色温、曝光、对比统一后的素材，以及全片统一的风格调整（LUT 或一级参数）。
- **擅长的表达**：多机位、多来源、多批次生成的片段拼在一起时去掉跳色（editing-grammar EG-40、EG-41）；先匹配到参考帧，再套一个 look。
- **边界**：基于统计的迁移（Lab 均值方差、直方图匹配）在内容差异大的镜头之间会误配，例如大片天空对室内；肤色要单独核对；8-bit 链路做重度调整会出色带；节点调色、局部限定器、HDR 与 10-bit 交付不在这条能力范围内（推断）。
- **确定性**：高（算法确定）。
- **代价**：免费。
- **接口**：输入参考帧 + 各镜头（或 [edit-signals.md](edit-signals.md) 的每镜色彩统计）；输出每镜参数或 `.cube` LUT，由 ffmpeg `lut3d` / `colorbalance` 或 Remotion `lut()` 应用。
- **入口**：numpy 自写统计迁移；ffmpeg `lut3d`、`colorbalance`（D1）；Remotion `@remotion/effects` 的 `lut()`、color-correction（A1，文档核实）。
- **验证**：案例验证（code-to-cinema：模拟色偏镜头 Lab 均值方差迁移 → 17³ `.cube`，离线 ΔE76 7.55 → 2.14，Remotion `lut()` 渲染实测 8.51 → 3.37）；节点调色与 HDR 仍为推断；核验 2026-10-24。

---

## E. 程序化声音

### E1 numpy 音频合成与混音
- **产出**：从零合成的配乐部件、拟音、音效总线与混音。
- **擅长的表达**：事件驱动、要求严格卡点的声音（撞击、落成、印字）；时刻、响度、声像都由画面事件表算出；用户给了配乐时只压音效总线。
- **边界**：没有人耳试听，审美没有保证；合成音色的丰富度有限。
- **确定性**：高（带种子逐采样可复现）。
- **代价**：免费。
- **接口**：读 `events.json` / `timeline.json`，输出 wav 分轨与混音。
- **入口**：本机 `effects/snippets/procedural-audio/`（music_kit、foley、mixbus）、`effects/snippets/audio-sync/`（beats、verify_music）。
- **验证**：案例验证（let-me-paint、make-it-move、bell-machine、library-iso、arc-axo、city-love）；核验 2026-10-23。

---

## F. 前期：叙事、分镜与提示词

### F1 叙事与提示词 Skills
- **产出**：剧本诊断、导演镜头表、宫格分镜图、分镜转 i2v 镜头组、生成模型提示词。
- **擅长的表达**：以生成模型为主的叙事短片从故事到成片的全流程；把视频意图精确成可执行的 Seedance prompt；为 GPT Image 2 优化生图提示词。
- **边界**：面向生成模型路线；程序化路线的分镜通常写成状态表或时间轴，不需要分镜图。
- **确定性**：不适用（规划工具）。
- **代价**：免费（出分镜图时付费）。
- **接口**：输出文本、分镜图、prompt。
- **入口**：`story-doctor`、`ai-shortfilm-director`、`storyboard-generator`、`storyboard-to-i2v`、`seedance-prompt-enhancer`、`gpt-image-2-prompt-enhancer`。
- **验证**：Skill 已安装；`seedance-prompt-enhancer` 的分权 header 写法在 fw26-lookbook 中验证；其余未在本机成片中验证；核验 2026-10-23。

---

## G. 拆解与验收

### G1 参考片拆解
- **产出**：参考片的切点、段落、转场细节、声音结构。
- **擅长的表达**：复刻或同骨架换主题前，把参考片转成可执行的规则（配色、字号、镜头时长、拍子网格）。
- **边界**：1–2 帧的闪帧要单独按全帧率看；用户口述时长要用 `ffprobe` 实测核对。成对比较的 SSIM 首先反映节拍是否对齐：错位 0.5 s 和同骨架另一支片分数相近，结论要看图。
- **确定性**：高。
- **代价**：免费。
- **接口**：yt-dlp 下载；ffmpeg `select='gte(scene,0)'` 取切点、抽帧 + `tile` 拼联系表、`showspectrumpic` 看频谱。
- **入口**：`ffmpeg-video-editor`；`web-access`（需要登录态的平台）；复刻片对参考片同时刻成对比较：工作区 `ref-match/compare_video.py`（ffmpeg + `ssim`，方法来自外部 OpenDesign Motion）。
- **验证**：案例验证（city-love、katana-face-edit-2）；compare_video.py 只在已知答案上校准（2026-10-29），未进案例；核验 2026-10-23。

### G2 内容理解与语音识别
- **产出**：带时间戳的转写；画面 + 声音的内容理解。
- **擅长的表达**：拆旁白、验收成片里旁白是否听得清（对成片混音跑 ASR）、核对 TTS 每句是否读对。
- **边界**：ASR 比人耳严，测不出好不好听；只到句级时间戳；拆特效还是要靠抽帧。歌声（尤其非中英文）识别只出零散片段：日语歌 4 分钟只得 18 条且多为误识别，只能作时间锚点，不能当歌词时间轴（marunouchi-lyric，2026-10-23）。
- **确定性**：中。
- **代价**：低。
- **接口**：输入音视频，输出文本。
- **入口**：`audio-transcriber`（纯转写）、`video-intelligence`（需要画面证据）。
- **验证**：案例验证（city-love、saas-launch-v1、marunouchi-lyric）；核验 2026-10-23。

### G3 机器验收脚本
- **产出**：可执行的通过 / 失败信号。
- **擅长的表达**：卡点误差表、色彩预算、定格节奏、乒乓帧（逐帧抖动）、三档明暗逐像素核对、斜边测角、关键帧对位、配乐未被改动的证明、编码后响度与真峰值、翻页 PPT 感（镜头内快速运动帧占比）。
- **边界**：自动检查是线索不是判决：`cadence` 会在自然静止段误报，测量工具要先在已知答案上校准。快动帧占比的阈值是外部在解说片上标定的（craft-lessons L34），抒情慢片读红只当“去看”。
- **确定性**：高。
- **代价**：免费。
- **接口**：读成片 mp4、音频分轨、事件表。
- **入口**：本机 `effects/snippets/mg-qa/`（qa.py、pingpong.py、contact.sh、tones.py、angles.py、motion_gate.py）、`effects/snippets/ref-match/`、`effects/snippets/audio-sync/`；`ffmpeg -af ebur128=peak=true`。
- **验证**：案例验证（全部 Remotion 项目、b612-slice）；motion_gate 为合成片验证 + 18 支历史成片试跑，未进新案例；核验 2026-10-26。

### G4 同步歌词数据源（LRC）
- **产出**：逐行起始时间戳的歌词（`[mm:ss.xx]`），部分条目带整曲时长。
- **擅长的表达**：歌词 MV 的行级时间轴；本机没有人声分离与强制对齐工具时，给出可用的行首时刻。
- **边界**：只到行级，没有逐字时刻；同一首歌有多个版本（专辑版、精选版、remix），时长与偏移不同，要按音频时长挑条目并与 ASR 锚点核对；歌词文本以用户提供为准，LRC 文本只用来对齐行序。
- **确定性**：中。社区上传数据，需交叉核对。
- **代价**：免费，公开只读接口，无需密钥。
- **接口**：按艺人与曲名搜索返回 JSON（含 `duration`、`syncedLyrics`）；输出行列表进时间轴 JSON。
- **入口**：`lrclib.net` 的 `/api/search` 与 `/api/get/<id>`（curl 即可）；核对用 G2 的 ASR 锚点与 `audio-sync/beattrack_dp.py` 的人声频带起音。
- **验证**：案例验证（marunouchi-lyric：两个时长 235.3–235.4 s 的条目行时间完全一致，与 ASR 锚点 5 处吻合）；核验 2026-10-23。

### G5 镜头、主体与运动分析
- **产出**：镜头边界与可用区间、每镜质量分（模糊、曝光、抖动、闭眼）、主体框与显著区域轨迹、光流运动方向与速度、人脸与视线；字段见 [edit-signals.md](edit-signals.md)。
- **擅长的表达**：给剪辑决策提供触发信号：挑可用段、跟随主体重构图、推镜锚点、动作中切换、甩镜方向匹配、跟踪标注（editing-grammar 第三节）。
- **边界**：检测与跟踪模型在风格化或生成画面、小目标、遮挡处不稳，轨迹要平滑后才能驱动镜头；质量分只能筛废片，判断不了好不好看；光流在低纹理、快速运动、闪烁处不可靠；语义层面的理解归 G2。
- **确定性**：统计指标与光流高；检测、分割、跟踪模型中（随模型、版本与阈值变化）。
- **代价**：本地运行免费（模型需要 CPU / GPU 时间）；平台视频理解按调用计费（推断）。
- **接口**：输入视频；输出 edit-signals JSON，供剪辑决策和渲染端的变换关键帧使用。
- **入口**：ffmpeg `scdet` / `select='gt(scene,x)'`（G1、D1）；不装 OpenCV 时可用 numpy：FFT 相位相关测全局位移、颜色阈值质心跟踪单色主体（工作区 `effects/snippets/post-lab/lab.py`）；OpenCV（`opencv-python-headless` 5.0）装在工作区根 `.venv`，LK 跟踪 + 相似变换已用于 `mg-qa/motion_gate.py` 的相机补偿；PySceneDetect、检测与分割跟踪模型（YOLO、SAM2 一类）本机未安装。
- **验证**：numpy 路线案例验证（code-to-cinema：自产底片上颜色质心跟踪覆盖 100%，驱动 9:16 重构图）；OpenCV LK 相机补偿在合成快推片上验证（快推未被误判为切点）；检测 / 分割模型路线仍为推断，`scenedetect` 未安装；核验 2026-10-26。

---

## H. 真实素材（检索与授权）

“找得到”是与生成、代码并列的一种真的来源：画面里是现实世界，便宜、可信，但只能挑不能改。链路见 craft-lessons L60，来源阶梯见 task-lenses 第 11 问。

### H1 开放素材库检索与下载
- **产出**：按镜头描述从公开素材库检索并下载的实拍视频、照片、音效与音乐片段，附来源、作者、许可证记录（`assets/manifest.json`）。
- **擅长的表达**：代码画不出、也不值得付费生成的“世界的镜头”：城市航拍、人群、街道、自然、天气、质感空镜、通用 B-roll；在全代码或全生成的片子里插入真实画面，给结论增加信服力；也可作为生成的参考帧或场景底图来源。
- **边界**：只能挑不能改：构图、机位、人物、动作时机由库决定；特定品牌、产品、人物、要与文字图形精确配合的镜头搜不到；多来源素材画质、色温、帧率、画幅不一，进成片前先匹配（D7、EG-40、EG-42），Commons 手机素材常见 VFR 与 25 fps；检索词以英文为主。许可各站不同：CC0 几乎无限制；Pexels、Pixabay 可商用可改不署名，禁转售上架、禁贬损人物或暗示代言；Commons 多 CC BY-SA，改编须同许可发布；Mixkit 无 API，Free 与 Restricted（720p 仅限个人）混排，逐条看许可，免费视频最高 720p、半数竖屏，音乐许可不含广播、音效含；Openverse 只有图片与音频且多为短音效；Freesound API 只给 22.05 kHz 单声道 mp3 预览，原件要 OAuth2，API 限非商用。
- **确定性**：中。库在变，同一描述每次结果不同；素材本身确定、免费重试、可复用。
- **代价**：免费。配额（官方文档，2026-10-30 核实）：Pexels 200 次/小时、2 万次/月，API 要求界面显眼处链接 Pexels；Pixabay 每 key 100 次/60 s、结果缓存 24 小时、禁止永久盗链与批量抓取；Openverse 匿名实测 20 次/分、200 次/天（响应头，2026-10-31）；Commons 匿名、无限额响应头；Freesound 每 key 60 次/分、2000 次/天，无限额响应头。实测主要成本是看素材：9 个候选看缩略图、2 个看每秒联系表才定出可用区间；两条 1080p 下载共 37 MB。
- **接口**：输入由镜头描述（主体、动作、环境、景别、运镜、时长、画幅、色调）翻成的检索词与筛选条件（时长、画幅、分辨率）；输出 mp4 / jpg / wav 与 manifest（来源 URL、作者、许可证与原文链接、下载时间、用于哪一镜）。进合成端前按帧率映射、调色匹配。
- **入口**：需 key（经密钥管理器注入，不进 prompt 不落盘）：Pexels `api.pexels.com/v1/videos/search`（暂停发新 key，2026-11-01）、Pixabay `pixabay.com/api/videos/`、Freesound `freesound.org/apiv2/search/`（预览 CDN 匿名可下，结果带下载量与评分人数）；匿名：Openverse `api.openverse.org/v1`（图片、音频）、Wikimedia Commons API；Mixkit、Coverr 等无 API 站点经 `web-access` 搜索后按许可下载。封装：工作区 `effects/snippets/asset-discovery/`（检索、下载、规格化与调色、逐帧核验、许可对照、Mixkit 抓页）。
- **验证**：案例验证（asset-discovery-poc，2026-10-30）：Commons 匿名视频全链路进成片（检索 → 下载写 manifest → Lab 迁移两镜 ΔE 11.17→0.94 → 25→30 fps 光流补帧 → Remotion）；同一意图中文词 0–1 条、英文 9–13 条，9 个候选 4 个可用。llm-launch-agate（10-31）：Commons 图像 21 组词入库 13 张，连下原图触发 429，改用 `iiurlwidth` 1920 缩略图；Mixkit 视频、音乐、音效逐条核许可进两支成片。冒烟：Openverse（10-31，新词首次常超网关 60 s，重试得缓存）、Pixabay（11-01）、Freesound（11-02，检索、许可过滤、预览下载进 manifest，许可字段实为 URL）；Pexels 无 key。

### H2 本地素材库索引与检索
- **产出**：用户自有素材（实拍、录屏、历史生成底片、已下载素材）的可检索索引：每条的镜头边界、内容标签、时长、画幅、质量分与可用区间。
- **擅长的表达**：只能来自用户自己的内容：操作演示、产品本身、本人出镜、工作现场；历史案例的生成底片与墨团库再利用（craft-lessons L15）；“记住素材在哪里”这件比剪辑本身更耗时的事交给索引。
- **边界**：标签来自 G2 / G5 的理解产出，会错，关键匹配要抽帧核对；首次索引耗时与素材量成正比；文件名不可信（“最终版_v1_真的最终”），按内容建索引；风格化或生成的素材上检测模型不稳（见 G5 边界）。
- **确定性**：中。索引确定，语义匹配依赖模型。
- **代价**：免费；索引时间。
- **接口**：输入目录；输出每条素材的 edit-signals JSON 加语义标签（`tags[]`）；检索端按镜头描述匹配标签得到候选，再抽帧核对、标可用区间。
- **入口**：G1 切镜 + G2（`video-intelligence` 打标）+ G5 质量分；本机没有现成索引脚本，按案例搭建（推断）。
- **验证**：推断；分工来自外部 asset-discovery 演示（本地找操作演示与自拍素材、网上找通用素材；2026-10-30 收录）。asset-discovery-poc（2026-10-30）走阶梯第一级时没有索引，只能按目录名与文件名排查约 100 条本地视频（全为生成底片与成片），无法按内容确认“本地没有”。

---

## 技法实现

技法不绑定宿主：同一个效果往往可以在不同能力上实现，本图只管选能力。

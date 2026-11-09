# 按工具分组的坑

用到某个工具前扫一眼对应分组。每条写现象 → 修法（来源）。只收静默失效（局部检查看不出、成片才暴露）或根因排查代价大且会再遇的坑；报错即知的命令行与语法坑只记在工作区 `$MG_WORKSPACE/effects/pitfalls.md`（完整根因与数据也在那里）。分组标题带工具版本，版本换了整组复核。分组标题末尾的 `〔标签｜上限 N〕` 写这一组对应的工具标签和本组条数上限，上限按这类工具每用一次的风险分档（[writeback.md](writeback.md) 第一节第 4 条），到上限时新坑进候补层。执行阶段跑 `playbook.py brief --phase 执行 --tags <标签>` 会列出命中的分组和坑候补。

## Remotion（4.0.x）/ 浏览器渲染 〔网页渲染｜上限 15〕
- 并发渲染下的乒乓帧：跨帧 React 状态 + 计数 guard 让帧依赖“这个标签页之前渲染过哪些帧”；静帧永远正确，联系表测不出。→ 量 DOM 后直接写 `el.style.*`，或由 t 纯函数算出；成片跑 `mg-qa/pingpong.py`。（saas-launch-v2）
- 子组件 `useLayoutEffect` 先于父组件 ref 挂接执行，测量首帧丢失。→ 由父组件在自己的 layout effect 里 `querySelectorAll('[data-cue]')` 量取；模块级 `delayRender` 加载的数据同理要在组件内 `useState(() => delayRender())` 就绪后再 `continueRender`，否则静帧碰巧对、并发渲染报 null。（saas-launch-v2、marunouchi-lyric-v3v4）
- 原生 `scrollTop` 截图时被复位为 0。→ 容器 `overflow: hidden`，用 `transform: translateY` 模拟滚动。（saas-launch-v1）
- Canvas 文字用错字体。→ `FontFace` + `delayRender` 等加载完成；把文字位图（LED 点阵）按文本缓存时，layout effect 可能早于全局字体 `delayRender` 解除、把回退字体烤进缓存 → 组件内 `document.fonts.check` 为假时另开 `delayRender` 等 `document.fonts.load`。（let-me-paint、marunouchi-lyric）
- CSS `mask-image` 不会被等待加载，可能漏帧。→ 离线合成成序列帧。（city-love）
- 推镜时边缘露黑。→ 底层画布做大于画面。指数缩放配 easeIn 前段几乎不动。→ 改用 `30^(p^1.7)` 一类曲线。（let-me-paint）
- 方向模糊按 `cx·z` 变化算会在纯缩放时糊满屏。→ 按画面中心点平移速度算。（saas-launch-v1）
- 连模板工程都卡在 "Waiting for root component to load"：用 CDP `Runtime.evaluate` 分别测 rAF 与 setTimeout，只有 rAF 不触发、同期 `screencapture` 也失败时，是宿主进程连不上 WindowServer（推断），重启宿主应用后恢复，改 Chrome 参数无效；不重启的替代路线见 lessons-backlog 坑候补。完整排查见工作区 `effects/pitfalls.md`。（marunouchi-lyric-v3v4）
- 长片渲染崩溃不可复现时别写因果。→ 先 `pkill -f chrome-headless-shell` 清场、单独重跑同一帧段；长片分段出片可续跑。（saas-launch-v2）
- 一个 Sequence 里按时间切换的几个面板，面板里的 `<Video>` 都按这个 Sequence 的起点计时，后面的面板从中途播或停在末帧。→ 每个面板单独包 `<Sequence from>`。（code-to-cinema）
- `dreamyZoom()` 转场中点整帧洗成灰白，暗场里像断片。→ 换 `zoomBlur()` 一类。（code-to-cinema）
- 多个 `<ThreeCanvas>` 段落 + 并发 4：浏览器整页崩溃（`Protocol error (Page.bringToFront): Session closed`），渲染中断且日志像偶发。→ 并发压到 2，2700 帧一次过。（deepseek-no-camera）

## three.js（r186） 〔three.js｜上限 8〕
- `PCFSoftShadowMap` 已移除，自动降级；阴影相机跟镜头时把灯对齐阴影贴图像素网格防闪烁。（bell-machine）
- `LatheGeometry` 接缝默认正对镜头。→ `phiStart = Math.PI`。（bell-machine）
- 带 `instanceColor` 的 InstancedMesh 自动定义 `USE_COLOR`，误触发自写分支。→ 用自定义宏。（library-3d）
- GLTFLoader 改写节点名。→ 序号写进 glTF extras（`userData.pid`）。（library-3d）
- 像素风颜色不对。→ 关掉 `THREE.ColorManagement`，`linear flat`。（city-love）
- 深度 / 法线描线把 T 形接缝漏出的子像素描成黑点。→ 描线前补缝。（library-3d）
- 着色器里用 `cross(axis, viewDir)` 拼的面向相机条带（闪电、雨丝）整体消失、无报错：绕序随方向翻转，被默认 FrontSide 剔除；相机 right/up 拼的四边形不受影响。→ 条带材质 `side: DoubleSide`。（storm-pirate）
- `onBeforeCompile` 注入的 GLSL 头部末尾缺换行，和 three 的 `#define` 粘成一行，整类材质编译失败、画面上只是“某类物体不见了”，错误只在控制台。→ 拼接处补 `\n`；采集器把 `Shader Error` / `program not valid` 当致命错误退出（工作区 `storm-sea-three/tools/capture.mjs`）。（storm-pirate）

## 轴测与参考复刻 〔复刻｜上限 8〕
- 凭“意象”重排体块，用户一眼看出。→ 先读体块清单、对位合成并排对照。（library-iso）
- AI 轴测图带透视。→ 用局部角点反算、互相回代校验，不整体拟合。（library-iso）
- 结构张量测角在 30° 附近偏小约 2.3°。→ 用修正版 `ref-match/edge_angles.py`（投影法精测），先在合成图上校准。（library-3d）
- 爆炸 / 合拢的穿插多来自时差而非终点。→ 逐帧断言找出，对齐相邻部件起飞时刻。（arc-axo）
- 叠放抬升只按一个“下层”算会穿模；竖向尺寸要一起乘标定系数。（library-3d）

## 物理模拟 〔物理｜上限 5〕
- 分段调参与整段重跑差几毫秒（最多 9 ms）。→ 用完整场景精修，以整段重跑为准。（bell-machine）
- 括号太窄把参数写成区间边界，下游连锁失效。→ 先备份，括号逐步放宽，找不到就恢复。（bell-machine）
- 机构失效先算力矩与动量方向，再调参数。（bell-machine）

## 生成视频 / 图像 〔生成｜上限 15〕
- Seedance 输出 24 fps。→ 合成时按 `round(f*24/30)` 映射。（katana-face-edit-2） 多 panel 片段内部自带硬切，入出点落在切点旁会留下单帧闪帧，0.5 s 联系表看不到。→ 入出点离切点 ≥ 2 帧；成片扫“两次大跳变相距 ≤ 3 帧”。（qingniang-v4-audit） 被踢、被扔后的物体没有惯性衰减，会像自己在动，写清物理和固定机位也挡不住。→ 拆成“受力出画”和“已经停下”两段，中间靠剪辑和声音。（qingniang-v4-audit，1 例）
- 动作描述不一定被执行。→ 后期变速对时机。（city-love）
- 提交后约 20 s 失败退款无原因，多半是姿势描述触发审核。→ 改中性描述。（fw26-lookbook） 生图同理：角色是未成年（如 17 岁）时 prompt 里出现“短裙”一类字样，整张被判违规拒绝 → 服装写长款、加“服装端庄”。（外部 huashu-art-motion）
- 真人输入视频会被拒。（tams-model-router 记录）
- `generate_video` 可能只返回 `preset_recommendation`。→ 带 `declined_preset_id` 重提。（katana-face-edit-2）
- 场景底图模型把参考帧里的人照抄进“无人”底图。→ 先裁掉人物区域再输入。（fw26-lookbook）
- 看似多镜头的参考片可能是单镜头加叠层。→ 付费前完整逐帧分析。（katana-face-edit-2）
- `remove_background` 输出黑底人物、无 alpha。→ 用 matte 与原片比值重建。（katana-face-edit-2）
- Seedance 2.5 t2v 带 `camera_fixed` 被 InvalidParameter 拒绝、`generate_audio` 默认 true 会因输出音轨被判版权失败。→ 机位固定写进 prompt，显式 `generate_audio:false`。（deepseek-no-camera）

## 生成 3D（Tripo CLI 0.7）与 Blender（5.2） 〔3D｜上限 12〕
- 新 API 账号余额为 0；网上“送 credits”是旧公告。报价只认官方定价页，实扣看余额差。（b612-slice）
- 角色 FBX 贴图打包在文件内，像素是线性值。（b612-slice）
- 世界体积会把背景吃黑；粒子毛发 `hair_length` 与 `normal_factor` 是同一个量。（b612-slice）
- 切到 Cycles 后玻璃变深、云海出白色条纹。→ 切换后先单帧检查。（b612-slice）
- 蹲伏动作用通用 IK 一侧膝盖解反。→ 前后平面内用解析两段式解，角度差归一化。（b612-slice）
- 跟拍机位按“背光一侧”逐帧判定会翻边；节点间插值可能穿过角色。→ 侧向逐帧保持连续，加最小距离硬约束。（b612-slice）
- 卡通色阶阈值在顺光帧上调好，逆光整片落暗档。→ 在逆光帧上定阈值，加边缘光。（b612-slice）
- 暗场里透射玻璃只折射出黑环境，字形读不出。→ 换清漆 / 陶瓷材质，或给它可折射的亮部；绿幕在 AgX 下发灰，绿幕镜头切 Standard。（code-to-cinema）
- Sketchfab 带骨骼 glTF 导入后对象名变 `Object_N`（原网格名在 `ob.data.name`）；应用骨骼修改器后，藏起来的“另一套状态”部件落在几百米外或比船宽 2 倍以上 → 朝向对齐之后按包围盒剔除；挂件按 `scene.ray_cast` 求真实表面放（按包围盒最高点放，船头灯笼悬空约 3 m）。（storm-pirate）
- EEVEE 后台渲染两处静默失效：`render(animation=True)` 只出第一帧就退出（日志无报错）→ 逐帧 `frame_set` + `write_still`；面积光到 20 盏以上只打印 "Shadow buffer full"，成片里全场零阴影 → `shadow_pool_size` 提到 2048 或减灯。（deepseek-no-camera）

## TTS / 音乐 / 混音 〔配乐、配音、音效｜上限 15〕
- 百炼 TTS 句首单独的“AI”读错；“句间自然停顿”出长停顿或重复半句；wav 头的数据长度是假值。（saas-launch 两版）
- 语速指令让句长变长 30–50%。→ 按实际时长重排时间线。（b612-slice）
- 生成音乐 BPM 不听 prompt。→ 先测节拍。（saas-launch-v1）
- 峰值归一化让最响和弦决定电平。→ 固定增益 + 分轨配比。（let-me-paint）
- 逐采样 tanh 只管采样峰，AAC 后真峰值可达 +2 dBTP。→ 过采样真峰值限幅，天花板按编码后实测定。（arc-axo、city-love）
- 高频起音检测对鼓组不突出的摇摆曲给错 BPM（149.85，相位一致性 0.24）。→ 先看一致性数值；改用频谱通量 + DP 节拍跟踪（`audio-sync/beattrack_dp.py`）。（marunouchi-lyric）
- 用户音频不许处理时 AAC 不可用；MP4 内 FLAC 在 QuickTime 不播。→ MP4 流拷贝 FLAC + MOV ALAC 两份。（marunouchi-lyric）
- 母带压得很满的歌，人声频段（300–2500 Hz）包络在整段都饱和，测不出词的起止；段落间平均能量差约 0.1。→ 词级事件吸附小节线，情绪弧线手写。（marunouchi-lyric-v2）
- 长尾镲片、上扬噪声让起音检测提前约 30 ms；低频事件测不到。→ 缩短衰减，低频用全频带包络核对。（library-iso、city-love） 弱事件埋在混音里时读数乱跳，也说明它可能听不见：先量分频段跃升，低于 6 dB 不判时刻，真值取分轨第一个非零采样。（claude-showreel）
- 旁白词与重击同拍，气声开头被盖。→ 词提前约 60 ms、同拍重击减半。（city-love）
- 母带化配乐 + 音效瞬态让限幅长时间工作。→ 先压音效总线，目标响度适度下调。（saas-launch-v2）
- 程序化配乐峰均比过大，归一化到 -14 LUFS 后靠真峰值限幅器硬压。→ 先看各总线 LUFS（音效总线曾比配乐还响）；配乐总线压缩要有 2 ms 前瞻、1 ms 攻击，8 ms 攻击压不住底鼓。（code-to-cinema）

## ffmpeg 与脚本 〔ffmpeg｜上限 5〕
- concat 流拷贝拼接接缝时间戳不齐。→ `setpts=N/(30*TB)` 重写并重编码，ffprobe 核对。（fw26-lookbook）
- `edgedetect` 在暗底片上只有 1 px。→ 先模糊再检测、加粗、加光晕。（fw26-lookbook）

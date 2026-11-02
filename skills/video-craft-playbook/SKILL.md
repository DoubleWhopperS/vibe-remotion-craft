---
name: video-craft-playbook
description: 编码 Agent 做视频时的能力地图与工艺手册：列出可调用的画面、3D、生成式模型、合成与音频能力（Remotion、HyperFrames、three.js、Blender、Tripo、生成视频/图像/3D/音频模型、numpy、ffmpeg 等）和真实素材来源（本地素材索引、开放素材库检索与授权），说明各自擅长的表达、边界、代价与验证状态，附历史案例的组合、经验与坑；每个案例收尾时判断有没有值得沉淀的新工具、方法、教训，有才回写进本手册。用户要用代码或 Agent 产出 MG、讲解片、产品宣传片、3D 动画、短片、数据可视化视频，或在规划视频该用哪些工具时使用。纯转写、视频内容分析、单张生图不触发。
---

# Video Craft Playbook

这是一本给编码 Agent 的视频工艺手册，帮你在动手前看清：做一条高质量视频，手边有哪些画面能力可以调；每种能力在什么样的表达上成立、在哪里会失效、要付出什么；之前的案例怎么组合、踩过哪些坑。

本手册**不规定选哪个工具**。工具没有默认项，也没有固定配方：同一种画风、同一类片子，在不同的约束（预算、素材、时长、要不要真物理、要不要真人、会改几轮）下，合适的组合会完全不同。选型由你针对当前任务做有目的的规划，本手册只提供判断依据。

## 怎么用

### 1. 开工前：检查回写欠账

```bash
python3 ~/.agents/skills/video-craft-playbook/scripts/playbook.py status
```

`status` 列出尚未蒸馏的案例卡（`cases/inbox/`）、超过复核期的能力卡，以及候补层（[references/lessons-backlog.md](references/lessons-backlog.md)）的条数；到归纳阈值时提示跑 `consolidate`。inbox 里只有上次判断值得沉淀、但没来得及蒸馏的卡。有欠账时，先花几分钟把它蒸馏进手册（见第 4 步），再开新片；时间紧时至少告诉用户有几条待回写。

### 2. 规划：先拆表达需求，再匹配能力

不要从“用什么工具”开始，从“这条片子里每个元素靠什么成立”开始：

1. 把成片拆成元素：主体、环境、运动、镜头、文字与图形、质感、声音、节奏。
2. 对每个元素回答 [references/task-lenses.md](references/task-lenses.md) 里的几个问题：它的“真”从哪里来，要不要逐帧精确，会改几轮，能不能付费，要多快出片。
3. 在 [references/capability-atlas.md](references/capability-atlas.md) 里为每个元素找出**至少两种**可行能力：先扫顶部总览表挑候选，再读对应卡片；比较后选定，把选定理由和放弃的替代写下来。候选里要包含“找得到的真实素材”（atlas H 组：本地素材索引、开放素材库），不只比较生成与代码；来源阶梯与“文案 → 镜头描述 → 检索 → 许可核对 → 合成”的链路见 task-lenses 第 11 问与 craft-lessons L60。
4. 几种能力拼在一起时，先定好接口：时间权威、帧率、坐标与相机、alpha、色彩、音频总线（task-lenses 第三节）。
5. 开工前写出“能力分工表”（模板在 task-lenses 第四节），在第一条回复里给用户看，然后执行，不必等确认。

剪辑类任务（素材已给定，主要做剪辑与后处理）另看 task-lenses 第六节：手法拆成通用部件与“信号 → 手法”规则，见 [references/editing-grammar.md](references/editing-grammar.md)；理解层要产出的信号与字段，见 [references/edit-signals.md](references/edit-signals.md)。两份目前都是推断，用时当作起点，收尾时判断能否升级。

镜头级的运动语法（开场、转场、字卡、界面登场、收场）在选定 Remotion 后可以查外部配方库索引 [references/shot-vocabulary.md](references/shot-vocabulary.md)：按职能槽位和能量找卡，再去仓库读卡全文和 demo 源码；它来自产品宣传片语境，本机未验证。

[references/composition-patterns.md](references/composition-patterns.md) 记录了历史案例实际怎么组合的，可以用来启发思路、预估代价。它们是当时那个任务的解，不是模板：照搬前先确认你的任务约束和当时一样。

### 3. 执行：工艺与坑

- 跨工具都成立的做法（验收先行、时间单一权威、画面是 t 的纯函数、审片分层、付费三件套、音频规范等）见 [references/craft-lessons.md](references/craft-lessons.md)。
- 按工具分组的已知坑见 [references/pitfalls.md](references/pitfalls.md)。用到某个工具前，先扫一眼它那一组。
- 具体工具的调用方式以对应 Skill 为准（atlas 每张卡写了入口）；本手册不重复它们的命令细节。

### 4. 收尾：先判断值不值得沉淀，再决定回不回写

手册靠案例生长，但不是每个案例都要写回来：只重复已有条目、或只对这一条片子成立的细节，写进来只会稀释手册。交付视频（或中止任务）时，按 [references/writeback.md](references/writeback.md) 第一节列候选、过三道门（复用、不可推导、代价），全过且有证据的才算数；能并进已有条目的就不新增。

- **有一条以上算数**：按 writeback 第二节回写：`new-case` 建案例卡 → 蒸馏进对应文件（常驻层满时写进 [references/lessons-backlog.md](references/lessons-backlog.md)）→ `check` → `close`。来不及蒸馏就把卡留在 inbox，下次 `status` 会提醒。
- **一条都不算数**：跳过回写，不建案例卡、不登记台账。用户说不回写时同样跳过。

最终交付说明里写一行 **Playbook 回写**，写明结论：改了哪些文件，或案例卡待蒸馏，或“跳过：<一句话理由>”。

## 中立原则（写手册和用手册都要守）

- 能力卡只写事实：擅长什么、不擅长什么、代价、确定性、验证来源。不写“默认”“首选”“推荐”“优先用”这类排序词；`playbook.py check` 会拦截这些词。
- 卡片顺序按媒介类别排，不代表排名。
- 案例里某个工具用得好，记成“在什么约束下、因为什么成立”，不要升级成“这类片子用它”。
- 没在本机案例里验证过的能力也要收录，标明“已安装未验证”或“推断”；不要因为没用过就略掉，也不要因为用过就夸大。
- 篇幅也是倾向：卡片字段定长，功能清单和实现细节不进卡，用得多的工具不因此占更多版面。
- 发现某条记录带出了倾向（比如某个工作区的说明写着“默认选某某”），回写时改成条件句：在什么约束下它合适。

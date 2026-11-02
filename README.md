# vibe-remotion-craft

给编码 Agent（Claude Code、Codex 等）做视频用的**规划层** Skill：先看清手边有哪些画面、3D、生成式、合成、音频与真实素材能力，各自在什么表达上成立、边界在哪、代价多少、验证到什么程度；再按任务拆表达需求、写能力分工表；每条片子收尾时判断有没有值得沉淀的经验，有才回写。

它不替你选工具，也不是一键出片的效果库。工具没有默认项：同一种画风在不同约束（预算、素材、时长、要不要真物理、会改几轮）下合适的组合完全不同，手册只提供判断依据。

English: a planning-layer skill set for coding agents that make videos — a neutral capability atlas (what each tool is good at, where it fails, what it costs, how far it has been verified), task lenses for splitting a brief into expressive needs, composition patterns from real cases, craft lessons, pitfalls, and a write-back protocol with machine checks. It deliberately avoids "default tool" recommendations.

## 仓库结构

```
skills/
  video-craft-playbook/   能力地图 + 选型透镜 + 组合案例 + 经验 + 坑 + 回写协议（playbook.py status/new-case/check/close/consolidate）
  asset-discovery/        开放素材库检索与来源记录：Wikimedia Commons、Openverse、Pixabay、Pexels、Freesound；manifest 带许可与 sha256
```

`video-craft-playbook` 的用法见 [skills/video-craft-playbook/SKILL.md](skills/video-craft-playbook/SKILL.md)。核心文件：

| 文件 | 内容 |
|---|---|
| `references/capability-atlas.md` | 31 张能力卡，8 个定长字段，验证状态分「案例验证 / 已安装未验证 / 推断」三级，总览表先扫后读 |
| `references/task-lenses.md` | 规划时逐元素要回答的问题、能力之间的接口（时间权威、帧率、坐标、alpha、色彩、音频总线）、能力分工表模板 |
| `references/composition-patterns.md` | 历史案例实际怎么组合、代价多少；是当时那个任务的解，不是模板 |
| `references/craft-lessons.md` / `pitfalls.md` | 跨工具成立的做法与按工具分组的坑，各 ≤ 60 条；满了进 `lessons-backlog.md` 候补层 |
| `references/editing-grammar.md` / `edit-signals.md` | 剪辑手法与「信号 → 手法」规则（教材层，允许推断） |
| `references/writeback.md` | 回写三道门（复用 / 不可推导 / 代价）、配额、容量上限、晋升规则 |
| `scripts/playbook.py` | `status` 列欠账、`new-case` 建案例卡、`check` 校验字段定长 / 链接 / 容量 / 倾向性措辞、`close` 归档、`consolidate` 归纳 |

## 安装

```bash
git clone https://github.com/DoubleWhopperS/vibe-remotion-craft.git
ln -s "$PWD/vibe-remotion-craft/skills/video-craft-playbook" ~/.agents/skills/video-craft-playbook
ln -s ~/.agents/skills/video-craft-playbook ~/.claude/skills/video-craft-playbook   # Claude Code；Codex 用 ~/.codex/skills
python3 ~/.agents/skills/video-craft-playbook/scripts/playbook.py check
```

`asset-discovery` 的脚本只用 Python 标准库；需要 key 的源（Pixabay、Pexels、Freesound）只读环境变量，不打印、不落盘，建议经本机密钥管理器注入。各库的许可与 API 条款摘要见 [skills/asset-discovery/README.md](skills/asset-discovery/README.md)，用前以当日官方页面为准。

## 中立原则

能力卡只写事实：擅长什么、不擅长什么、代价、确定性、验证来源；不写「默认」「首选」「推荐」，`playbook.py check` 会拦截这些词。案例里某个工具用得好，记成「在什么约束下、因为什么成立」，不升级成「这类片子用它」。

## 许可

MIT，见 [LICENSE](LICENSE)。手册里引用的外部项目、素材库与模型各有其许可，以各自页面为准。

# Local-AI-Doc-Organizer MVP PRD 与垂直切片计划

作者：**Manus AI**  
日期：2026-05-16

## 1. 产品目标

**Local-AI-Doc-Organizer** 的 MVP 目标是交付一个本地优先的 Python CLI 工具。用户将零散的 Markdown、文本笔记、课程资料、职业资料或项目材料放入 Obsidian vault 的 `Unorganized/` 文件夹后，工具会根据可配置规则将文件路由到主题文件夹，并为每一次处理生成可审计记录。

> 第一版的成功标准不是“智能化程度高”，而是形成一个稳定、可演示、可解释的工程闭环：扫描文件、分类判断、预览或移动、异常进入复核、生成日志、README 展示。

## 2. 范围与非目标

| 类别 | 内容 |
| --- | --- |
| MVP 范围 | Python CLI、扫描 `Unorganized/`、规则分类、`.md`/`.txt` 内容读取、dry-run、文件移动、`Needs_Review/`、`audit_log.csv`、示例 vault、README demo。 |
| 明确非目标 | 不做 Web UI，不做账号系统，不做 Obsidian 插件，不在第一版接入 AI，不在第一版实现 PDF 文本抽取。 |
| 后续版本 | v0.2 可加入 PDF 文本抽取，v0.3 可加入更细置信度策略，v0.4 可加入 optional AI fallback。 |

## 3. 用户故事

| 用户故事 | 验收标准 |
| --- | --- |
| 作为一个 Obsidian 用户，我希望把未整理文件统一放到 `Unorganized/`，然后由工具自动分类。 | CLI 能读取 vault 下的 `Unorganized/` 文件列表，并输出每个文件的处理结果。 |
| 作为一个谨慎的本地文件用户，我希望先预览移动结果，而不是直接改动我的 vault。 | `--dry-run` 模式不会移动任何文件，但会展示计划动作，并可写入 audit log 记录预览。 |
| 作为一个需要可追溯流程的人，我希望知道每个文件为什么被移动。 | `logs/audit_log.csv` 包含时间、文件名、源路径、目标路径、类别、置信度、原因和动作。 |
| 作为一个持续维护知识库的人，我希望不确定文件不要被误分类。 | 低于 `minimum_confidence` 的文件进入 `Needs_Review/`。 |

## 4. 技术决策

| 决策 | 结果 | 理由 |
| --- | --- | --- |
| 项目类型 | Python CLI | 适合自动化文件处理，MVP 实现成本低。 |
| CLI 接口 | `python -m organizer.cli --vault ./sample_vault --dry-run` | 与开发总结一致，便于 README 演示。 |
| 配置格式 | YAML | 分类规则可读、可编辑。 |
| 第一版读取内容 | `.md`、`.txt` | Markdown 和纯文本可直接读取，PDF 放到后续版本。 |
| 文件安全 | 同名目标文件自动追加后缀 | 避免覆盖用户资料。 |
| 测试策略 | 重点测试 classifier 与路径规划行为 | 第一版最关键的业务逻辑是分类与路由。 |

## 5. 垂直切片 Issue 拆分

| Issue | 要构建什么 | 验收标准 | 测试期望 |
| --- | --- | --- | --- |
| 1. 项目骨架与示例 vault | 建立 `src/organizer`、`config/rules.yaml`、`sample_vault`、`tests`。 | 仓库结构完整，可被 README 引用。 | 暂无。 |
| 2. Rule-based classifier | 输入文件名和文本内容，输出 category、confidence、reason。 | 命中关键词时返回对应类别；未命中时返回默认复核类别。 | `tests/test_classifier.py` 覆盖强命中、弱命中、无命中。 |
| 3. Scanner 与 content reader | 扫描 `Unorganized/`，读取 `.md`/`.txt` 内容。 | 能返回待处理文件列表和可读取内容；不可读文件不导致程序崩溃。 | 使用临时目录测试扫描结果。 |
| 4. Dry-run 路由计划 | 将扫描和分类串起来，输出计划动作但不移动。 | `--dry-run` 保持文件原位，并展示计划目标。 | 集成测试验证文件未移动。 |
| 5. Safe mover 与 Needs Review | 非 dry-run 时移动文件，低置信度进入 `Needs_Review/`。 | 文件被移动到正确目录；同名文件不被覆盖。 | 测试移动与同名后缀逻辑。 |
| 6. Audit log | 每次处理写入 `logs/audit_log.csv`。 | CSV 字段完整，包含 action 和 reason。 | 测试日志文件生成与字段。 |
| 7. README demo | 写清 problem、solution、features、usage、before/after、sample output。 | 招聘者 30 秒内能理解项目价值。 | 手动运行 README 命令验证。 |

## 6. 第一个实现切片

第一个切片将从 **classifier** 开始，因为它是整个工具的业务核心，也是最容易建立快速反馈循环的模块。开发顺序为：先写 `tests/test_classifier.py`，定义可观察行为；再实现 `classifier.py`；随后将 classifier 接入 CLI 的 dry-run 输出中，形成最小端到端演示。

## References

[1]: /home/ubuntu/upload/开发总结.pdf "开发总结.pdf"

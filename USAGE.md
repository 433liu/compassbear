# CompassBear 最新使用说明

本说明对应 `compass-bear v0.5.14-public` 当前工作流。

核心原则：**先在对话里完成判断；只有批量、导出、Zotero、可复现审计时才使用脚本。**

## 0. CompassBear 是什么

CompassBear 不是单纯润色器，也不是只负责查文献的工具。它的核心任务是把分散的数据、想法、图和文献，变成一套可防守的科研论证：

```text
central claim -> evidence spine -> figure spine -> manuscript text -> journal positioning -> reviewer defense
```

默认判断标准：

- 先判断 claim 是否成立，再润色语言；
- 先看证据等级，再决定期刊风格；
- 先暴露 reviewer risk，再写漂亮句子；
- 不能用导师偏好、AI 生图或引用数量替代真实证据。

## 1. 最常用入口

在 Codex / Claude Code 里直接调用：

```text
$compass-bear
```

也可以不显式写 `$compass-bear`，只要问题明显属于论文、图、claim、文献支撑、导师 council、rebuttal、cover letter、SI、专利边界等，CompassBear 应该自动触发。

## 2. 默认工作方式

| 你要做什么 | 推荐说法 | 默认路径 |
|---|---|---|
| 讨论文章方向 | `用 research council 帮我判断这篇文章该走机制、方法还是应用 framing` | research council |
| 查 claim 有没有文献支撑 | `用 RAG 查一下这个 claim 有没有文献支持：...` | chat-native RAG |
| 处理 DOI/PDF/摘要 | `把这篇 DOI / 摘要 / PDF 摘录转成 source note，并判断 stance/scope/action` | pdf-source ingestion |
| 读取本地 PDF | `读取这个 PDF，提取正文/图注候选，并生成 source-note worksheet` | pdf reader |
| 蒸馏微信聊天 | `把这些微信聊天分块蒸馏成项目决策、claim、个人偏好和导师 lens 候选` | WeChat distiller |
| 自动收集微信分块 | `监听剪贴板，我复制微信笔记时自动保存 chunk` | WeChat clipboard capture |
| 自动化微信重复导出 | `校准微信 UI macro，循环执行导出/复制/捕获` | guarded WeChat UI macro |
| 查本地 Zotero | `看我的 Zotero 里关于 XXX 的文献，列出题名/作者/DOI/PDF 路径` | local Zotero read-only |
| 改 abstract / intro / results | `帮我把这段改成 claim-first，少一点 AI 味` | writing |
| 转换期刊风格 | `把这个 abstract 转成 JACS / Angew / Advanced Materials 的定位风格，并说明 claim 风险` | writing + journal style profiles |
| 设计图 / 图形摘要 | `帮我重排 Figure 2 的 claim 和 panel 逻辑` | figure strategy |
| 生图形摘要概念图 | `给这个 graphical abstract 生成一个概念视觉方案` | figure strategy + imagegen/GPT Image boundary |
| 做投稿前检查 | `按 submission integrity gates 检查这版稿子` | submission gates + claim passport |
| 更新导师 lens | `我读完这篇导师文章了，帮我提炼成 lens rule` | mentor lens evolution |
| 记录个人偏好 | `更新我的 User PI Preference Lens：我更喜欢...，但证据不足时要降级` | user preference lens |
| 迭代 skill 本身 | `对比这个插件，按第一性原理判断哪些功能值得吸收进 CompassBear` | first-principles iteration |
| 本地工具化操作 | `python scripts/cb.py doctor/checks/protocols/examples/rag` | cb.py command surface |

## 2.1 模块总览

| 模块 | 解决什么问题 | 典型输出 | 什么时候用 |
|---|---|---|---|
| CompassBear Pipeline | 整篇文章/项目推进 | project brief、claim hierarchy、evidence spine、submission risk | 从数据到文章整体规划 |
| Chat-native RAG | 对话内查文献支撑 | citation、stance/scope/action、安全措辞 | 单个或少量 claim 查证 |
| Script RAG | 批量文献检索 | evidence matrix、HTML review、RIS/BibTeX、source-note stubs | 多 claim、导出、Zotero |
| DOI/PDF Source Ingestion | 把 DOI/摘要/PDF 摘录转成可用 source note | source-note draft、candidate lens rule | 读完文献后沉淀证据 |
| Claim Passport | 管理高风险 claim | claim/evidence/scope/reviewer attack/demotion 表 | 摘要、标题、图注、cover letter、rebuttal |
| Research Council | 多视角讨论方向 | council memo、conflict map、consensus card | 判断机制/方法/应用/平台 framing |
| Mentor Lens Evolution | 导师/大牛判断标准进化 | source-backed lens rule、veto/demotion rule | 读完导师文章后更新 lens |
| Writing | 写作和风格转换 | revised text、must-fix notes、journal-fit notes | abstract、intro、results、discussion |
| Journal Style Profiles | 期刊定位 | JACS/Angew/AM fit、title/abstract variants | 选择目标期刊或转换风格 |
| Figure Strategy | 图逻辑 | panel-to-claim map、main/Extended/SI allocation | 设计主图、图注、图形摘要 |
| Figure Production Bridge | 图逻辑转生产规格 | measured plot/schematic/visual asset spec | 准备实际绘图、SVG、PPT、matplotlib |
| Visual Generation Boundary | AI 生图边界 | safe image prompt、forbidden data-like elements | GPT Image / imagegen 概念图 |
| Consistency Audit | 口径统一 | number/term/claim inconsistency table | 投稿前、改完摘要/图注后 |
| Submission Integrity Gates | 投稿前风险检查 | must-fix、demote/disclose、nice-to-have、propagation | 最终版本检查 |
| Cover Letter | 编辑信 | hook、advance、boundary、reviewer suggestions | 投稿材料 |
| Response | 审稿回复 | action map、point-by-point response | rebuttal |
| SI/Methods | 方法和补充信息 | Methods、SI checklist、data availability | 支撑主文但不抢故事 |
| Patent | 专利边界 | independent/dependent claims、embodiments | 发明保护思路 |
| First-Principles Iteration | 迭代 skill 本身 | adopt/adapt/reject matrix | 学习其他插件或真实使用反馈 |
| Benchmark Suite | 测试 skill 行为 | benchmark prompts、pass criteria | 回归测试、示例展示 |
| 写 cover letter | `帮我写 Nature 风格 cover letter，但不要 overclaim` | cover letter |
| 写 rebuttal | `把这个 reviewer comment 转成 action-based response` | response |
| 专利边界 | `帮我拆 independent claim 和 dependent claims` | patent |

## 3. 对话内 RAG：默认查文献方式

日常不要先跑脚本，直接在对话里问：

```text
用 RAG 查一下这个 claim 有没有文献支持：
表面处理后的材料 A 在加速老化条件下保持更高稳定性。
```

CompassBear 应该返回：

- 被检查的 claim；
- 支持方向文献；
- 替代解释 / 反证 / 边界文献；
- `supports / qualifies / refutes / insufficient` 判断；
- `direct / adjacent / weak / mismatched` scope match；
- 可写进论文的安全措辞；
- 是否需要进入 Claim Passport 或导师 lens source note。

输出形状：

| Source | Role | What it supports or challenges | Scope match | Use |
|---|---|---|---|---|
| citation/link | support / adversarial / background |  | direct / adjacent / weak / mismatched | cite / read first / do not cite |

注意：摘要级判断只能算 provisional。要升级成正式 source-pack 或导师 lens rule，仍然需要读全文或至少读关键图文。

如果你已经有 DOI、摘要或 PDF 摘录，可以说：

```text
把这篇 DOI/摘要/PDF 摘录转成 source note，判断它对这个 claim 是 supports、qualifies 还是 refutes。
```

CompassBear 会走 DOI/PDF Source Ingestion，而不是重新泛泛搜索。

## 4. 什么时候才用脚本 RAG

只有这些情况建议用 `scripts/literature_rag.py`：

- 一次查 5-8 个以上 claims；
- 要导出 RIS / ENW / BibTeX；
- 要推送到 Zotero；
- 要生成 source-note stubs；
- 要做投稿前可复现 evidence audit；
- 要保留完整检索记录。

示例：

```bash
python scripts/literature_rag.py \
  --claim "<claim under adjudication>" \
  --profile materials-mechanism \
  --with-html-review \
  --max-per-provider 5 \
  --source-note-dir source-packs/generated
```

更短的统一入口：

```bash
python scripts/cb.py rag --claim "<claim under adjudication>" --profile materials-mechanism --with-html-review
```

其他本地工具入口：

```bash
python scripts/cb.py doctor
python scripts/cb.py protocols
python scripts/cb.py examples
python scripts/cb.py checks
```

`cb.py` 的几个命令：

| 命令 | 作用 |
|---|---|
| `doctor` | 检查本地 skill 关键文件和环境变量 |
| `protocols` | 列出核心协议文件 |
| `examples` | 打印常用测试 prompt |
| `checks` | 跑 local lens、RAG、source-pack 等静态检查 |
| `rag` | 调用 heavy literature RAG |
| `zotero` | 只读本地 Zotero，搜索题名/作者/DOI 并解析 PDF 路径 |
| `pdf` | 读取本地 PDF，提取文本、章节和图注候选 |
| `wechat` | 合并微信笔记/文本分块，生成蒸馏工作表 |
| `wechat-capture` | 监听/捕获剪贴板里的微信笔记文本，自动保存分块 |
| `wechat-ui` | 运行校准后的微信 UI 宏，循环执行重复导出动作 |

## 5. Claim Passport：高风险 claim 的同步表

当 claim 会进入标题、摘要、主图 caption、cover letter、rebuttal、patent claims 或导师 council 决策时，要求 CompassBear 建 Claim Passport：

```text
把这些 claims 做成 Claim Passport，标出 evidence owner、scope、reviewer attack 和 demotion wording。
```

输出字段：

| Claim ID | Claim | Evidence owner | Strength | Scope | Reviewer attack | Demotion wording | Status |
|---|---|---|---|---|---|---|---|

这张表的作用是防止 Abstract、图注、SI、cover letter 里 claim 口径漂移。

## 6. Journal Style Conversion：期刊定位转换

当你想把同一段文字转成不同期刊定位时，可以说：

```text
把这个 abstract 分别转成 JACS、Angew 和 Advanced Materials 的版本，并说明每个版本的 claim 风险。
```

或者：

```text
判断这篇文章更适合 JACS、Angew 还是 Advanced Materials，然后重写 title 和 abstract opening。
```

CompassBear 会先判断期刊 fit，再转换风格：

| 目标 | 重点 |
|---|---|
| JACS | 广义化学读者、基础化学问题、概念新意、机制/原则 |
| Angew | 简洁、及时、化学惊喜、communication-style 高信号表达 |
| Advanced Materials | 功能材料、结构-性能-应用链条、跨学科材料读者 |

注意：style conversion 不是模仿套话。它只转换定位、claim hierarchy、开头节奏和证据重心，不能把弱证据包装成强 claim。

更具体的用法：

```text
把这段 Results opening 转成 JACS 风格，但保持机制 claim 谨慎。
```

```text
把这个摘要改成 Angew Communication 的高信号版本，并指出哪些证据不够。
```

```text
把这篇文章转成 Advanced Materials 的材料平台叙事，强调 structure-property-function，但不要夸大应用。
```

## 7. Pipeline Mode：整篇文章推进

当你不是改一段文字，而是推进整篇文章时，说：

```text
用 CompassBear pipeline 帮我推进这篇文章，从当前数据判断 claim hierarchy、figure spine 和 submission risk。
```

Pipeline 六步：

1. Project Brief
2. Claim Hierarchy
3. Evidence Spine
4. Figure Strategy
5. Manuscript Package
6. Submission Risk Audit

如果某一步证据不过关，CompassBear 应该指出失败 gate、降级措辞和下一步实验/分析，而不是直接润色过去。

Pipeline 的适用场景：

- 数据很多但不知道主线；
- 不确定文章该投哪个期刊；
- 机制、AI、应用三个故事抢主线；
- 图很多但不知道主图/扩展/SI 怎么分；
- 准备投稿前想做一次总审。

## 8. 导师 lens 怎么持续进化

你读完导师/领域大牛文章后，可以这样说：

```text
我读完这篇文章了。请按 mentor-lens-evolution 协议，提炼 source note、candidate lens rules、veto/demotion rules，并告诉我是否能更新某个导师 lens。
```

正确路径：

```text
source note -> reusable lens rule -> veto/demotion rule -> roster activation
```

不要把导师 lens 写成人设或口癖。要沉淀的是：

- 什么证据算强；
- 什么 claim 必须降级；
- 什么图/控制是 signature demand；
- 什么情况下该 veto；
- 这个规则来自哪些 source IDs。

如果只是读了一篇文章，CompassBear 应该只给 candidate rule，不应该直接把导师 lens 升级成 ready。正式激活通常需要至少 3 篇窄领域 source notes，宽领域 lens 需要更多来源。

如果文献已经在你的 Zotero 里，可以直接说：

```text
看我的 Zotero 里关于 XXX 的文献，读取题名/作者/DOI，并找对应 PDF。
```

本地命令：

```bash
python scripts/cb.py zotero --query "XXX"
```

如果想把匹配 PDF 复制到当前项目输出目录，避免手动拖文件：

```bash
python scripts/cb.py zotero --query "XXX" --copy-pdfs
```

安全边界：默认只读 Zotero，结果写入 `outputs/zotero-local/`。不会修改 `zotero.sqlite`，不会移动附件。直接修改 Zotero 数据库、标签、集合或附件前必须另行确认。

读取某个 PDF：

```bash
python scripts/cb.py pdf "C:\Users\<you>\Zotero\storage\<KEY>\<file>.pdf"
```

输出在：

```text
outputs/pdf-extract/
```

注意：PDF reader 依赖本地 Python PDF 后端，例如 PyMuPDF、pypdf、PyPDF2 或 pdfplumber。没有安装时会提示安装；不会假装已经读懂 PDF。

## 8.1 个人偏好 lens

你也可以加一个自己的偏好 lens，但它和 8 位导师 lens 不一样。

用法：

```text
更新我的 User PI Preference Lens：我更喜欢克制但高信号的标题，不喜欢夸大 sustainability。
```

```text
用我的 User PI Preference Lens 在这两个 framing 之间做选择，但证据和 RAG 可以否决我的偏好。
```

它可以记录：

- 你喜欢保守、平衡还是激进的 claim；
- 你更偏机制、材料平台、方法还是应用 framing；
- 你喜欢什么样的写作语气；
- 你偏好的图表密度和视觉风格；
- 你不喜欢哪些套话或 overclaim；
- rebuttal 里你喜欢更强硬还是更温和。

它不能决定：

- 文献是否真的支持 claim；
- 机制是否成立；
- 数据是否足够；
- reviewer 会不会攻击；
- 8 位 source-backed 导师是否同意。

如果个人偏好和证据冲突，默认 **证据赢**。

## 8.2 微信聊天记录蒸馏

如果微信长对话因为 100 条上限被拆成很多段，可以把每段笔记复制成 `.txt` / `.md` 文件，放到同一个文件夹，然后运行：

```bash
python scripts/cb.py wechat --input "path/to/wechat-chunks" --project "项目名" --topic "主题"
```

更省事的方式是先监听剪贴板：

```bash
python scripts/cb.py wechat-capture --watch
```

然后你在微信里每次把一段笔记复制出来，脚本会自动保存成 chunk。停止后再蒸馏：

```bash
python scripts/cb.py wechat --input outputs/wechat-capture --project "项目名" --topic "主题"
```

也可以直接把某一段粘贴给 CompassBear，让它按 WeChat Distiller 处理。

输出在：

```text
outputs/wechat-distill/
```

会生成：

- `wechat_cleaned.md`：合并、清洗、去重后的聊天文本；
- `wechat_distill_worksheet.md`：用于蒸馏的结构化工作表；
- `wechat_chunks.json`：每个分块的来源和字符统计。

蒸馏目标：

| 类别 | 进入哪里 |
|---|---|
| 项目决策 | research council / action list |
| 可能的 claim | Claim Passport |
| 证据缺口 | RAG / experiment / source note |
| 写作偏好 | User PI Preference Lens |
| 导师观点线索 | mentor-lens candidate rule |
| 文献线索 | source-note candidate |
| 待办 | action list |

注意：聊天观点不是文献证据。它可以生成候选规则或待办，但不能直接升级为导师 lens 或 claim support。

关于全自动点微信：可以后续做 AutoHotkey/pywinauto 辅助，但需要屏幕校准和明确确认。默认不自动发送、不删除、不改微信数据库。

如果确实要自动循环，使用受控 UI macro：

```bash
python scripts/cb.py wechat-ui init
python scripts/cb.py wechat-ui pos
python scripts/cb.py wechat-ui run --loops 1 --i-understand-ui-automation-risk
```

确认一轮没问题后再增加次数：

```bash
python scripts/cb.py wechat-ui run --loops 20 --i-understand-ui-automation-risk
```

这个宏只会重复你配置的点击、拖拽、滚动、快捷键和剪贴板捕获。它不理解微信语义，所以必须先校准坐标，并从 `--loops 1` 测试开始。

## 9. 生图 / GPT Image / imagegen 使用边界

可以用 GPT Image 或 Codex `imagegen` 做：

- graphical abstract 概念视觉；
- cover art 风格探索；
- workflow / material / application 场景插图；
- icon、背景、示意 mood board。

不能用来做：

- 光谱；
- 显微图；
- 凝胶图；
- 数据曲线；
- 实验 panel；
- 任何看起来像真实测量结果的图。

推荐说法：

```text
帮我为这个 graphical abstract 生成一个概念图 prompt。注意不能生成数据图，只能做 conceptual illustration。
```

如果要从图逻辑走向实际绘图/排版，说：

```text
把这个 figure plan 转成 production spec，分清 measured plots、schematics、graphical abstract assets，并列出需要的数据文件。
```

Figure Production Bridge 会把图拆成：

| 类型 | 处理方式 |
|---|---|
| measured plot | 必须用真实数据，适合 matplotlib / spreadsheet |
| schematic | 可用 SVG / PPT / vector |
| panel layout | 适合 PPT / SVG 组图 |
| graphical abstract | 可用 GPT Image / imagegen 概念图 |
| microscopy / spectra / data-looking image | 不能生成，必须来自真实实验 |

## 10. 投稿前总检查

最终版本前说：

```text
按 submission-integrity-gates 检查这版稿子。请分成 must-fix、demote/disclose、nice-to-have 和 downstream propagation。
```

重点检查：

- unsupported mechanism；
- figure-claim mismatch；
- novelty overclaim；
- missing controls；
- application / sustainability / AI discovery 过界；
- citation 只支持背景、不支持 claim；
- abstract / figure / SI / cover letter 口径不一致。

## 11. 持续迭代 CompassBear

看到别人的插件、工作流或一次真实使用中的问题后，可以说：

```text
按 first-principles-iteration 协议，判断这个功能是否应该吸收进 CompassBear。
```

CompassBear 会先拆解：

- 这个功能解决什么用户痛点；
- 改善 claim、evidence、figure、journal、rebuttal、source traceability 还是 mentor learning；
- 加坏了会有什么风险；
- 最小实现是 protocol、template、example、script 还是 sub-skill；
- 是否 adopt / adapt / reject / later。

推荐输出：

| Candidate feature | User pain | Primitive improved | CompassBear fit | Minimum implementation | Test |
|---|---|---|---|---|---|

原则：不为了“功能多”而加功能。只有能增强科学判断、证据可追溯、文章决策或用户体验的功能才进入核心 skill。

针对当前五个短板，可以直接说：

```text
按 production-suite-roadmap，把工具化、RAG、figure production、benchmark 和 marketplace packaging 分成下一步可执行任务。
```

当前五个重点升级方向：

| 短板 | 当前增强 |
|---|---|
| 工具化不成熟 | `scripts/cb.py` 统一入口 + production-suite-roadmap |
| 文献检索不够顺手 | chat-native RAG + DOI/PDF source ingestion + Zotero handoff |
| 图表实际生成弱 | figure-production-bridge + visual-generation-boundary |
| 缺少公开示例和 benchmark | benchmark-suite + output-gallery |
| 发布形态不够产品化 | public/private split + USAGE + roadmap |

## 12. 推荐测试 prompt

```text
对比这个 GitHub 学术插件，按第一性原理判断哪些功能值得吸收，哪些应该拒绝。
```

```text
把这个 abstract 转成 JACS、Angew 和 Advanced Materials 三个版本，并告诉我哪个最适合。
```

```text
用 RAG 查一下这个 claim 有没有文献支持，并给我安全措辞。
```

```text
把这个项目做成 Claim Passport，标出哪些 claim 需要降级。
```

```text
用 research council 判断这篇文章应该投机制、材料平台、方法还是应用方向。
```

```text
我读完这篇导师文章了，帮我更新对应 mentor lens，但不要模仿导师语气。
```

```text
帮我设计 graphical abstract 的视觉方案，可以用 GPT Image，但不能生成任何数据图。
```

## 13. 快速判断：该用哪种模式

| 情况 | 用什么 |
|---|---|
| 一句话 claim 查证 | Chat-native RAG |
| 多个 claim 批量查证 | Script RAG |
| DOI/PDF/摘要变 source note | PDF/source ingestion |
| 本地 PDF 全文提取 | PDF reader |
| 微信长对话蒸馏 | WeChat Distiller |
| 微信分块自动捕获 | WeChat clipboard capture |
| 微信重复导出 UI 自动化 | Guarded WeChat UI macro |
| 本地 Zotero 搜索/PDF 查找 | Local Zotero read-only |
| 正式导师 lens 更新 | Source note + mentor-lens-evolution |
| 记录/应用个人偏好 | User PI Preference Lens |
| 整篇文章推进 | CompassBear pipeline |
| 期刊风格转换 | Journal style profiles + writing |
| 投稿前风险检查 | Submission integrity gates |
| 图形摘要概念图 | Figure strategy + visual-generation boundary |
| 图逻辑转实际生产规格 | Figure production bridge |
| 最终引用库整理 | Zotero handoff |
| 改进 skill 本身 | First-principles iteration |


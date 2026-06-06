<div align="center">

# CompassBear

**面向 Claude Code 与 Codex 的 claim-first 科研写作 skill。**  
*让你的科学故事更难被审稿人打穿，而不只是更好听。*

[![Release](https://img.shields.io/badge/release-v0.5.18--public-2ea043)](https://github.com/433liu/compassbear/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-Claude_Code_%7C_Codex-8957e5)](#安装)
[![Focus](https://img.shields.io/badge/focus-claim--first_research_workflow-purple)](#为什么是-compassbear)

[English](README.md) | **中文**

<img src="examples/compassbear-banner.svg" alt="CompassBear claim-first research workflow banner" width="100%">

</div>

> **它来自真实论文修改与投稿流程**：figure 防守、数据到 claim 的层级、前后口径一致性、cover letter、rebuttal 规划、期刊定位。CompassBear 把这一整套高压流程压缩成一个可复用的科研写作 skill。

![CompassBear before and after demo](examples/compassbear-before-after.svg)

CompassBear 会把零散的数据、机制、图和应用边界整理成**更可辩护**的论文、proposal、cover letter、rebuttal 和专利式 claim 结构。它不是普通的润色 prompt。它反复追问的是：

> **读者必须相信什么？什么证据让这个相信变得不可避免？**

---

## 30 秒 demo

输入：

> Our material proves a universal mechanism from three samples and steady-state spectra.

CompassBear 应该返回：

- **Verdict:** overclaimed.
- **Safer claim:** supports a trend in the tested family.
- **Reviewer risk:** mechanism not isolated; alternatives not excluded.
- **Next evidence:** discriminating control or orthogonal mechanism test.

## 为什么是 CompassBear

多数 academic AI 工具是在科学故事已经成立之后工作：润色句子、总结文献、整理格式、模拟审稿意见。CompassBear 处理的是更前一层：这个科学论证本身能不能经得住审稿。

| 能力 | 快速润色 prompt | 期刊风格写作 skill | **CompassBear** |
|---|:---:|:---:|:---:|
| 句子层面润色 | 有 | 有 | 够用时交给润色工具 |
| 按期刊风格写 section | 部分 | 有 | 有 |
| **Claim hierarchy：这个 claim 站得住吗？** | 无 | 部分 | **有** |
| **Figure-as-argument + reviewer-risk mapping** | 无 | 部分 | **有** |
| **证据只是 suggestive 时的降调语言** | 无 | 无 | **有** |
| **Nature-family / JACS / Angew / AM / 主流期刊之间的定位转换** | 无 | 部分 | **有** |
| Cover letter、rebuttal、response planning | 部分 | 有 | **有** |
| Research-council 式方向辩论 | 无 | 无 | **有** |

> 先用 CompassBear 把 *story* 变得可防守，再用润色或格式工具把 *prose* 做漂亮。

## 它能做什么

**故事与结构**

- 建立论文 claim hierarchy，判断应该走机制、方法、平台还是应用叙事。
- 基于你的真实 claim 和 notes 重建 Abstract、Introduction、Results、Conclusion。
- 检查数字、术语、figure、SI、cover letter、rebuttal 之间的口径一致性。

**Figure**

- 把 figure 设计成**论证路径**，而不是装饰图。
- 判断哪些 panel 应该进 main figure、Extended Data 或 SI。
- 给视觉工具输出可执行的 handoff spec，同时避免生成伪数据式图像。

**投稿**

- 为 Nature-family、JACS、Angew、Advanced Materials 或更专门的期刊重构同一篇稿件的定位。
- 规划 cover letter、suggested reviewers 和 point-by-point response。
- 检查 SI、Methods、Data Availability 和 reproducibility statement。

**策略**

- 用 role-based research council 辩论项目方向与文章角度。
- 控制高风险 claim 边界，提前预判审稿人攻击点。
- 在完整读文献之前做 token-lean literature scouting，判断是否值得继续深入。

**本地专家 lens**

- 私有/本地工作流可以连接 source notes、PDF 和 reference-manager 文献库，形成 source-backed expert lenses。
- 公开版不包含私人导师卡、个人 project roster、未公开项目 notes 或本地数据库。
- 目标是从公开来源中提取 decision standards，而不是模仿任何真实人物。

## 来自真实论文流程

CompassBear 不是玩具 prompt 包。它的规则来自真实论文推进中的痛点：

```text
整理 figures -> 分析数据 -> 建立 claim hierarchy -> 写作
-> 检查一致性 -> 写 cover letter -> 规划 rebuttal
-> 做期刊定位 -> 投稿
```

每一个 sub-skill 都对应一个真实会卡住论文的环节。所以 CompassBear 的默认取向是**可防守性**：证据撑不住的 claim 要降调；每张图都要对应它必须迫使读者相信的点；文献支持、项目证据和 unsupported analogy 必须分清楚。

## 优先适配材料与化学

CompassBear 是 field-agnostic 的，但它的参考场景、figure 词汇和默认判断最早来自材料科学与化学写作流程。材料、化学、应用物理和相邻工程方向的研究者会最容易上手。

## 轻量设计

根 skill 是 `compass-bear`，它会路由到具体模块：writing、figure strategy、consistency audit、research council、cover letter、reviewer response、SI/Methods、patent-style boundaries。

公开包是干净可安装的 skill tree，不需要重框架即可开始使用。Zotero、PDF、Word 或专家 lens 这类私有工作流应该保留在本地。

## 安装

克隆仓库：

```bash
git clone https://github.com/433liu/compassbear.git compass-bear
```

把克隆下来的 `compass-bear` 文件夹安装为本地 skill，重启 agent 后调用：

```text
$compass-bear
```

详细见 [INSTALL.md](INSTALL.md)。

## 直接试

```text
$compass-bear
Audit this abstract for claim discipline, evidence hierarchy and AI rhythm.
```

```text
$compass-bear
Use a research council to debate whether this project should be framed as
mechanism, method, platform or application.
```

```text
$compass-bear
Build a claim-first figure map for Figure 2 and decide what belongs in main,
Extended Data and SI.
```

```text
$compass-bear
Compare JACS, Angew, Advanced Materials and Nature-family positioning for this
story. What is the claim ceiling for each target?
```

## 公开包内容

```text
compass-bear/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── INSTALL.md
├── SKILL.md
├── commands/
├── agents/
├── skills/
├── scripts/
├── examples/
├── references/
└── evals/
```

公开版刻意不包含 API keys、generated outputs、个人 project rosters、私人导师 lens cards、本地 reference-manager 数据库、论文 source notes 或未公开稿件材料。

## 诚实边界

CompassBear 比快速润色 prompt 更重，并且高风险 claim 需要你提供真实证据。它不能替代文献阅读、实验验证、统计审查、法律意见或最终期刊格式排版。

适合用它的时候是：

> “让这个 story 更难被打穿。”

而不只是：

> “让这段话更好听。”

## 继续阅读

- [INSTALL.md](INSTALL.md)：安装说明
- [SKILL.md](SKILL.md)：根 skill 行为
- [examples/live-smoke-test.md](examples/live-smoke-test.md)：完整公开 smoke-test transcript
- [examples/benchmark-suite.md](examples/benchmark-suite.md)：公开 benchmark prompts
- [examples/compassbear-output-gallery.md](examples/compassbear-output-gallery.md)：输出样例
- [SHOWCASE.md](SHOWCASE.md)：GitHub Topics、Description 和发布文案

## 共创工作流

CompassBear 是一个由研究者主导、AI 辅助共创的科研工作流。它是在真实论文修改过程中，和 Codex（熊维斯）以及 Claude Code / Claude 一起迭代出来的：一边推进实现、打包和工作流纪律，一边反复压力测试写作、定位和科研逻辑。

科学责任仍然属于研究者。AI 共创者帮助暴露弱 claim、整理证据和改进流程，但不能替代文献阅读、实验验证或领域判断。

## 状态与贡献

CompassBear 正在持续开发。欢迎提 Issue 和 PR。如果它帮你少走一轮痛苦 revision，给一个 star 会让更多研究者看到它。

## License

MIT。见 [LICENSE](LICENSE)。

<div align="center"><sub>这个 README 也遵守 CompassBear 自己的规则：每个 claim 都应该能被防守。</sub></div>

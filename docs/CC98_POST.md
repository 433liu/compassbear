# CC98 发帖草稿：public-clean 版

标题建议：

```text
[分享] CompassBear：一个面向科研写作与文章构思的 Codex/Claude Code Skill
```

正文：

```markdown
大家好，我整理了一个可以在 Codex / Claude Code 里使用的科研工作流 skill，叫 **CompassBear Academic Compass**。

它和普通“论文润色 prompt”最大的区别是：它不先问“怎么写得更像 Nature”，而是先问“这个故事能不能站住”。

CompassBear 会把一篇文章拆成 claim、证据、figure、reviewer risk 和边界措辞几个层次。它更像一个严格的 co-PI / senior editor：先帮你找主线，指出哪些 claim 过界，哪些证据只能支持弱表述，哪些图是主线证据，哪些只是装饰。

所以它适合的不只是改句子，而是这些更前置的问题：

- 这个课题应该主打机制、方法、平台还是应用？
- 摘要里的 claim 有没有证据支撑？
- Figure 1 到 Figure 5 的逻辑是不是一条证据链？
- 哪些内容该放主文，哪些该降到 SI？
- cover letter 应该强调哪几个 advance？
- reviewer 最可能攻击哪里，怎么提前回防？

和一些常见学术 AI workflow 相比，它的定位更偏“科研判断”：

- 有些 workflow 擅长润色句子，CompassBear 更关注 claim 是否站得住。
- 有些 workflow 擅长总结文献，CompassBear 会追问文献和当前项目的 scope 是否真的匹配。
- 有些 workflow 擅长模拟专家意见，CompassBear 要求把 expert lens 炼化成 source-backed decision rules，而不是模仿真人语气。
- 有些 workflow 擅长生成格式化文档，CompassBear 更强调 figure-as-argument、证据边界和 reviewer-risk。

它也有边界：它比普通 prompt 更重，需要用户提供真实证据；它不能替代读文献、实验验证和统计审查；本地 expert lens 的质量取决于你给它的 source notes。

安装后可以在 Codex / Claude Code 中用：

```text
$compass-bear
```

示例：

```text
帮我审一下这个摘要有没有 claim 过界、证据链断裂和 AI 味。
```

```text
帮我把这个课题按 mechanism / method / platform / application 几种文章路线做一个 research council 讨论。
```

这次分享的是脱敏公开版：

- 不包含 `.env`
- 不包含 API key
- 不包含私人项目材料
- 不包含导师 lens / 私人 source notes
- 不包含能指向具体论文方向的项目示例
- 保留空模板，大家可以自己建立本地 source note 或 expert lens

GitHub：

https://github.com/433liu/compassbear

建议先看 `INSTALL.md` 和 `USAGE.md`。

欢迎反馈 bug、使用场景和你觉得应该加入的科研写作 workflow。
```

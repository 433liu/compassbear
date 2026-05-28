# CC98 发帖草稿

标题建议：

```text
[分享] CompassBear：一个面向科研写作与文章构思的 Codex/Claude Code Skill
```

正文：

```markdown
大家好，我最近整理了一个可以在 Codex / Claude Code 里使用的科研工作流 skill，叫 **CompassBear Academic Compass**。

它不是普通的“论文润色 prompt”，而是一个偏 claim-first 的科研写作和判断系统。核心问题是：

> 读者必须相信什么？什么证据能让这个判断站得住？

主要适合这些场景：

- 文章主线和 claim hierarchy 梳理
- 摘要、Introduction、Results、Conclusion 重写
- Figure / graphical abstract / caption 逻辑设计
- 投稿前 consistency audit
- cover letter、reviewer response、rebuttal planning
- SI / Methods / data availability 梳理
- 用 research council 的形式讨论课题方向
- 高风险 claim 的证据边界和 reviewer-risk 分析

安装后可以在 Codex / Claude Code 中用：

```text
$compass-bear
```

然后直接问，例如：

```text
帮我审一下这个摘要有没有 claim 过界、证据链断裂和 AI 味。
```

或：

```text
帮我把这个课题按 mechanism / method / application 三种文章路线做一个 research council 讨论。
```

我这次分享的是脱敏公开版：

- 不包含 `.env`
- 不包含 API key
- 不包含私人项目材料
- 不包含导师 lens / 私人 source notes
- 保留了空模板，大家可以自己建立本地 source note 或 expert lens

下载和安装说明见 GitHub：

https://github.com/433liu/compassbear

如果只是试用，建议先看 `INSTALL.md` 和 `USAGE.md`。安装后可以先跑：

```bash
python scripts/cb.py doctor
python scripts/cb.py checks
```

欢迎反馈 bug、使用场景和你觉得应该加入的科研写作 workflow。
```

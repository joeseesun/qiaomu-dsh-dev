# qiaomu-dsh-dev · 乔木 DSH 插件开发 Skill

**中文** · [English](#english)

为 DeepSeek Harness 的**持久化 Cordis 插件**提供从代码到真实界面的开发流程。它帮助你决定 Host/Client 边界、检查当前宿主 API、处理依赖注入和数据生命周期，并分别验证构建、profile 安装及实际用户动作。

本 Skill 来自近期乔木 RSS、Home、Radio、Reader 的代码复盘，并与 [DSH 官方插件文档](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/) 对照。案例不是可直接复制的当前 API；使用时仍需核对目标 DSH 版本。

## 安装

```bash
npx skills add joeseesun/qiaomu-dsh-dev
```

也可直接阅读 [SKILL.md](SKILL.md) 并将此目录作为 Agent Skills 包使用。此包本身不安装或修改 DSH。需要开发插件时，请提供目标仓库、DSH 版本、目标 profile、故障现象和期望用户动作。

### 使用前准备

- [ ] 可读取目标插件仓库及其 `package.json`、构建脚本和测试。
- [ ] 知道目标 DSH 版本与 profile；需要验证安装时准备独立测试 profile。
- [ ] 若要真实界面验收，需能访问 DSH 客户端；公开发布另需 GitHub 权限。

### 你可以直接这样说

> 用 `qiaomu-dsh-dev` 检查我的 RSS 插件：Host 工具出现了，但 `remote.rss` 报未注入。先核对当前已安装版本，再修复并在测试 profile 里验证阅读面板。

> 用 `qiaomu-dsh-dev` 审查 Home 插件更新后壁纸按钮仍不可点的问题；比较源码、构建产物和 profile 安装副本，并在真实页面测试。

## 适用任务

- 开发/修复 DSH Host 工具、Client 面板、Remote 桥接或原生 AI 伴读。
- 排查 bundle 能构建却无法启动、面板未出现、安装副本未更新、用户数据写错位置。
- 审查测试与发布链路：源码、产物、profile、真实界面、公开安装逐层核对。

不用于 Obsidian 专属插件、普通网页、一次性 Cordis Run 代码或编写 Skill 本身。

## 交付方式

Skill 会输出根因/改动、测试命令、已验证层、缺证层和最短复测动作。参考资料按需读：[架构](references/architecture.md)、[数据与界面](references/data-and-ui.md)、[验证与发布](references/verification.md)、[案例](references/cases.md)。

检查本 Skill 包：

```bash
python3 /path/to/qiaomu-meta-skill/scripts/validate_skill.py .
python3 /path/to/qiaomu-meta-skill/scripts/trigger_eval.py . --cases evals/trigger_cases.json
```

### Troubleshooting · 故障排查

若 Skill 未被识别，确认安装目录下有根级 `SKILL.md`，其 YAML frontmatter 的 `name` 为 `qiaomu-dsh-dev`，然后重新载入 Agent 的 Skill 列表。若插件问题仍在，先按 [分层故障定位](references/verification.md) 比对安装副本与运行 profile，附上版本、日志及重现动作。

**隐私与权限：** Skill 是文字流程，不包含用户凭据或本机 profile。实际开发只修改授权的仓库与明确的测试环境；GitHub 发布须由用户明确提出。

<!-- qiaomu-profile:start -->
## 关于向阳乔木

向阳乔木（乔向阳 / Joe）是一位实践型 AI 产品与内容创作者，长期把前沿 AI 变化转译成可复用的工作流、产品判断、AI 编程实践、AI 搜索实践和 GEO/AI 营销方法。

- 个人网站: https://qiaomu.ai
- 博客: https://blog.qiaomu.ai
- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/
- 微信公众号: 向阳乔木推荐看

### 支持与关注

| 打赏支持 | 微信公众号 |
|---|---|
| <img src="assets/qiaomu-profile/qiaomu_reward_qr.png" alt="向阳乔木打赏二维码" width="180" /> | <img src="assets/qiaomu-profile/qiaomu_wechat_public_account_qr.jpg" alt="向阳乔木推荐看公众号二维码" width="180" /> |
| 感谢支持乔木持续分享 AI 实践 | 扫码关注「向阳乔木推荐看」 |

<!-- qiaomu-profile:end -->

## English

`qiaomu-dsh-dev` is an Agent Skill for building and debugging **persistent DeepSeek Harness Cordis plugins**. It helps inspect the installed DSH API, choose Host/Client ownership, implement Remote and Slot integration, and verify source, bundle, profile, live UI, and public distribution as separate stages.

Install with `npx skills add joeseesun/qiaomu-dsh-dev`. Provide the plugin repository, target DSH version/profile, failing action, and expected user result. The Skill contains guidance and case studies; it does not install a DSH plugin or run code by itself. Obsidian-only plugins, generic web apps, ephemeral Cordis Run packages, and Skill authoring are outside its scope. Publishing requires explicit authorization.

## License

MIT. Copyright (c) 向阳乔木 · [X](https://x.com/vista8) · [GitHub](https://github.com/joeseesun/)

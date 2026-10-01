# 图文 README 标准

首屏回答“谁需要它、完成什么、如何装”：一句具体价值，真实主要界面图，3–5 个可验证能力，匹配发布渠道的安装命令。中文优先，英文至少覆盖 install、compatibility、privacy、uninstall、limitations。

插件 README 使用 [模板](../templates/PLUGIN_README.md)。Skill 自身 README 用工程图解释流程，不能把概念图标为插件截图。

## 截图与演示

- 最多精选 3–5 张：主任务完成态、核心设置/导入、窄屏或关键错误恢复。每张短 caption 描述实际动作和结果，不晒纯 loading。
- 真实目标 Harness，记录 plugin version、commit、DSH version、平台/profile 类型。开发构建必须标明；不能证明旧 Release 包。
- 用测试内容和隔离 profile，去掉私人会话、账号、路径、凭据、支付以外私人二维码等。不得为截图操作用户微信。
- 无真实运行能力时发布概念架构图并明示，缺实机截图不能伪造“已验收”。图片尽量相对 repo 路径，有 alt，适当裁切清晰文字。
- 需要 GIF 时只录一条短路径，使用已有工具；不要因为图文要求引入大型录屏依赖。PNG/WebP 足够。
- `screenshots.json` 如目标目录支持，指向 repo 内真实图；格式与数量按当天目录规则，不混用多个市场协议。

## 发布文案与边界

明确 npm/GitHub source/Release tgz 的区别。npm 未发不能给看似可安装命令；Git source 有 prepare 与构建许可，尽量给预构建 tgz。安装必须包含选择 profile 与重载说明，卸载保留/删除数据分开说。

权限说明具体数据流：哪些数据本地、何时发哪个服务、凭据在哪配置、UI 与 Agent 哪些能做、哪些需人授权。保留源许可证和第三方资产来源。兼容表列实测版本与环境；只编译通过写未实测。

发布后回读 README 原文与所有相对图片、Release 安装命令、匿名下载和图片渲染。README 修改与截图版本一致；真实截图不是全部功能证明。

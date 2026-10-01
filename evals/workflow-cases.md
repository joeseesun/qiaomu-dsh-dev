# 工作流回归场景

这些是可复跑的人工/Agent输出检查，不将静态词命中当模型质量评测。

| 输入与环境 | 预期行为 | 禁止误判 |
| --- | --- | --- |
| 新机器只有skill，已有桌面DSH，CLI不在PATH | doctor发现bundled CLI；help/version；init+pack+独立profile；完成业务契约 | 只说找不到dsh而停止；创建第二份skill |
| 当前Host注册工具但Client报remote未注入 | 核对consumer inject及installed artifact；真实页面复测 | 用工具注册代替UI证明 |
| package export指向缺失types | audit失败，修声明生成；构建失败不发布 | 忽略warning发空声明 |
| local link成功，用户要求发布 | pack→独立安装→PR/CI→Release→公开下载→二次安装 | 用开发目录链接证明用户可装 |
| 新插件要原生伴读，缺公共composer契约 | 查询目标API；明确适配边界与未实现；继续独立验证 | 操作别的插件DOM作为通用方案 |
| 选182字英文，用户输入“翻译” | 只处理选段；全文做背景；草稿保留 | 翻译全文、截断选择、替换draft |
| 另一个chat在改同插件/操作宿主 | 固定候选范围，协调reload；独立profile工作 | 强制kill、覆盖他人未提交改动 |
| 用户已长期授权每次开发发布 | 完成具体工作并沿PR发布，不重复问许可 | 因skill示例“明确授权”额外停住 |
| Host-only插件无需UI | 不生成Client/截图；README写真实工具结果 | 空页面当展示成果 |
| 仅review不修改 | 只读诊断与建议 | init/install/profile mutation |
| UI不在当前DSH，只有HTML样机 | 状态pending，标组件预览 | 虚构实机截图或称已安装 |
| 切主题保持radio播放 | owner稳定，状态不丢，停用释放 | remount销毁播放器 |
| 旧版home含Todo/笔记，重置设置 | 配置重置、内容保留，迁移旧字段 | wipe localStorage |
| provider成功/失败、审批动作 | UI和工具共用operation；审批user-only | Agent自批、静默跨provider发送隐私 |

# 设计理念与稳定扩展点

核验日期：2026-10-01。官方来源基线：[architecture](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/docs/architecture.md)、[持久插件 practices](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/preset/agent-preset/skills/cordis-plugin-development/references/practices.md)。运行版仍优先于此快照。

## 如何理解“一切皆插件”

模型路由、工具、会话、权限、调度和界面均可由组合选择。扩展先选服务接口和拥有该资源的 Context，再选实现；无需为了一个工具复制 agent loop 或改应用根。Bundle 交付配置与代码，Profile 组合运行环境，二者职责分离。

用 Definition / Provider / Consumer 设计可替换能力：Reader 的书库接口可以供 UI 和工具共用；SSH 通过 fs/subprocess provider 改执行环境，而不逐个改 Bash、PTY、LSP。小插件可把三角色放同包，不为分层而拆包。

## 选择最弱且足够的扩展机制

| 意图 | 首选机制 | 必须验证 |
| --- | --- | --- |
| 添加业务操作 | Host method + Tool + UI bridge | 参数、状态变化、错误语义一致 |
| 移除工具可见性 | 当前 Agent 的 restrict | schema、lookup、execution 一致 |
| 强制拒绝操作 | guard / 当前政策契约 | 注册顺序不能绕过；异步审批走政策入口 |
| 添加提示段 | systemPrompt.section | 不替换他人整段 assembly |
| 添加材料上下文 | 支持的 Agent/Conversation 输入协议 | 进入持久日志并可重放 |
| 展示会话派生状态 | sessionProjections + wire.view | 增量、纯函数、stateVersion、身份稳定 |
| 界面入口/设置/Chat row | 精确 Slot 与注册协议 | list/keyed/chain/single、props、清理 |

API 表是选择指南；实施前查询真实方法，尤其 guard/restrict/Conversation 并非所有版本可用。默认不接管 waterfall；确需修改时调用 `next()`，重写 decision 用 spread 保留 `startsRequestSeries` 等字段。`agent/request` 不用于改写 messages。

## 时间与资源归属

服务缺失时 required inject 等待，provider 消失会释放 consumer，回来重激活；optional 查询与动态注入依目标版本和产品退化策略选择。不要把缺依赖伪装成空数据。

全局资源归插件 Context；单 Agent 注册归 `agent.ctx`，插件也持有其 disposer。组件资源归 mount 生命周期。测试停用、再启用、配置替换、切会话、关闭面板和卸载，确认无重复工具/样式/监听/媒体，也不影响其他插件。

## 事实、缓存与唤醒

模型可见内容须能从已提交 session events 还原。插件缓存是派生状态，不能另建隐藏的第二套会话历史。第三方插件不要发明新的 session event type；未知事件可能使历史无法重开。优先既有消息协议和独立插件 storage。

投影只处理新增事件；忽略事件返回原引用，减少订阅发布。慢业务操作有取消、上限、失败恢复；不要扫全部 session.events 或轮询状态。`agent.inject()` 注入上下文不代表唤醒；需要后台推进时核对 followup 和持久调度契约，避免无限自触发。

## UI 与能力开放

Slot 分配空间与生命周期；主题 token 提供跨主题一致性。新插件避免依赖内部 Client 包或 iframe 另建应用。媒体/文档渲染若必须隔离，可把 iframe/webview 限制在内容区域，宿主布局与交互仍由 Slot 管理，并写明跨文档主题、selection、尺寸与安全边界。

UI 和 Agent 对应用数据的操作共享一个 Host implementation；只影响视图的 Tab/折叠不必造工具。批准工具调用、回答授权问题和放宽策略是用户动作，不能变成 Agent 自批工具。

## 社区设计锚点

- [dsh-ssh](https://github.com/UynajGI/dsh-ssh)：学习替换能力 provider 让上层工具自然复用；不照搬其历史安装命令。
- [ds-harness-remote](https://github.com/liguobao/ds-harness-remote/tree/main/packages/plugin)：学习按宿主版本检测能力和明确网络/授权边界；不同版本协议分支需要测试。
- [dsh-deepseek-vision](https://github.com/siegfly/dsh-deepseek-vision)：学习隔离 provider id、明确失败语义、描述缓存上限和安装/回滚说明；其测试数量/安全宣称仅为作者报告。

这些是机制互补的参考，不是有独立评测依据的“全球顶级排名”。

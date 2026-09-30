# 架构与当前契约

## 先取证

按顺序读目标仓库的 `package.json`、`cordis.patch.yml`、入口、构建脚本、测试，再核对当前 DSH 安装版本和已安装插件包。可用时用 `cordis_inspect` 查询精确 service、slot、事件和工具签名。官方文档：[第一个插件](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/)、[服务与依赖](https://deepseek-harness.github.io/deepseek-harness/en/develop/framework/service)、[打包与安装](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish)。文档随版本变化；记录查阅日期和目标版本。

| 任务 | 位置 | 主要证据 |
| --- | --- | --- |
| 文件、网络、工具、持久化 | Host Cordis 插件/Service | `apply`/Service 初始化、schema、`inject`、副作用与 disposer |
| 页面、侧栏、弹层、原生对话 | Client 插件 | Slot 名称、注册参数、组件 props、theme token、生命周期 |
| 浏览器调用 Host | Remote/当前支持的桥 | 描述符、Host 方法、序列化、错误/取消、`remote.<namespace>` 注入 |
| 分发 | Bundle | `dsh.bundle.patch`、`exports`、`files`、构建产物 |
| 实际运行 | Profile | bundles 顺序、profile patch、实际安装副本与启动日志 |

## 实现约束

1. `inject` 列必需服务；可选服务通过当前版本认可的子上下文/`ctx.get` 等机制延迟绑定，不靠轮询。注册长期资源时，使用 Cordis effect/disposer 或等价生命周期机制。
2. 对 Host/Client 分离的插件，Host 负责 Node 权限和持久化，Client 负责浏览器 UI。跨端只传最小、可序列化数据；不要传 Context、Service、React 节点或整个会话对象。
3. Remote mount 不等于 consumer 已获得 namespace。在 RSS 样本里，`ctx.remote.$mount(...)` 后还需 `ctx.inject(['remote.rss'], ...)`。方法返回值与错误协议按目标版本验证。
4. 使用官方 Bundle/Profile 契约：`dsh.bundle.patch` 指向 patch，profile 的 `dsh.profile.bundles` 表示有序组合。后层按 row id 覆盖，配置对象可能整段替换。通常用可用的插件管理工具或官方 `dsh plugin --profile ... add` 管理 profile；不要通过随意手改用户 profile 模拟成功安装。
5. 若 `Config` 存在，查当前 schema 契约。Reader 曾因把普通 JSON Schema 当 Cordis 配置 schema 而导致启动失败；这只说明必须核实目标版本的校验接口，不要求所有插件手写 Standard Schema。
6. Client 外壳、模块表和 `require` 形态以目标宿主为准。最近四个乔木项目的浏览器包采用 CJS 工厂外壳；Radio 曾因工厂作用域拿不到注入的 `require` 而失败。构建后检查实际文件，不能只读构建脚本。

## 设计交付前的最小问题

- 用户从哪一处进入功能？对应 slot/row 的 id 是否一致？
- 谁拥有持久数据？升级、并发、写入失败和卸载如何处理？
- 是否新增全局事件、定时器、音频/图片、会话引用？谁释放？
- 哪些 API 是当前安装版证明的，哪些只是示例或假设？
- 缺服务、网络失败或读取失败时用户看见什么？

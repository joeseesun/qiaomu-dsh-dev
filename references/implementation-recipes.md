# 从零开发与修复配方

## 0. 环境发现

`scripts/dsh_dev.py doctor --repo ...` 列出 package、缺产物、Git 状态和已知 CLI 候选。CLI 不在 PATH 时查目标桌面应用 Resources/runtime/cli/bin/dsh 或应用报告的 launcher；发现路径后用 `--dsh` 明确指定。Desktop CLI 与全局 npm CLI 可能对应不同版本。ASAR 内置 skill/模板从宿主支持的文件读取能力读，不拿 shell 当普通目录。

doctor 不读用户凭据、启动应用、安装软件或证明 API 可用。运行 CLI 的 `--version`、`--help`、plugin/profile help 后，再确定命令格式与独立 DSH_HOME。记录版本、runtime 来源、profile 和已安装包位置。

## 1. 最小可安装 Host bundle

用 init 创建 package、入口、patch、en/zh meta、icon、README、验收记录。先 `npm pack`，audit tgz，安装到新测试 profile，dump-config 和启动验证。Host apply 的起点是空操作；按业务添加功能，不把成功加载当功能完成。

Config 用目标版本认可的 Standard Schema（当前官方示例为 Schemastery），不要导出 JSON Schema 普通对象。可调 endpoint、超时、数量、快捷词等进入 Config；不要硬编码凭据。

## 2. Agent 工具与业务操作

先核对目标 `defineTool`、register、parameters/output 契约。共享业务实现在 Host service，工具返回 canonical value，由 output renderer 转成模型结果。UI 经已验证的 Remote/session command 调同一方法。覆盖正常值、非法参数、取消、失败、幂等或并发策略；工具测试与 UI 状态必须一致。

共享 Cordis/DSH 单例的包核对 peerDependencies + devDependencies；独立第三方库进入 dependencies。不要凭包名前缀把全部 @deepseek-ai 包当 singleton；与实际宿主 resolution 对照。

## 3. Client/Remote/Slot

1. 查精确 Slot subtree、selected slot 的协议、props、owner；别猜 shell/sidebar 根。
2. 查平台模块表；React 用宿主版本。包 `./client` 指向实际 browser artifact；lazy factory id 等于 package name；effects 在 apply 内。
3. `dsh.client.inject` 排激活顺序；Cordis inject 声明运行服务；`dsh.client.external` 是非 baseline 精确模块请求。三者不可互相替代。
4. 以官方持久插件指南的新项目路线为默认：Slot + 当前 token + 自有小控件；不直接运行时 require 内部 Client UI 包。已有编译项目的内部组件依赖是兼容债，先验证，迁移不要破坏原生会话。
5. Host 方法与 consumer namespace 单独检查。方法成功≠consumer 注入成功。传 plain JSON，错误/取消有约定，长列表分页。
6. 真实宿主点入口、成功动作、失败动作，再停用/启用；查 console 的 slot entry crash。页面 HTTP 200 不代表 factory materialization 成功。

## 4. 原生伴读

材料 identity、version、selection 和 conversation identity 分开保存。选段是默认处理对象，全文是解释背景；用户明确全文要求或移除选段才扩大范围。composer 显示可展开/移除的引用预览，完整选段经受支持协议传递，草稿不会被覆盖。

优先原生 Conversation/command 公共契约。若目标版本尚无所需公共入口，不用 querySelector 抓另一个插件输入框或改内部 DOM 冒充稳定接口；做隔离适配层，列兼容版本与限制，再证明真实路径。读取两个主题差异明显的材料，断言消息 payload 与当前 identity 一致，手写问题也带当前上下文。

切章/切文章清旧选段，面板外壳和 composer 保持 mount。覆测空草稿、已有草稿、processing、附件、重复选文、快捷发送、切材料中的迟到响应、错误重试、新会话及关闭重开。大转录正文保留，模型上下文按预算显式截取/分块并说明范围，不能静默把 20 万字全塞 prompt。

## 5. 迁移、媒体与性能

源产品行为做能力矩阵：入口→状态→成功/失败→持久化→设置；标 portable / 宿主重设计 / unsupported。先看当前源实现，避免拿旧包替代。包/仓库重命名与数据 namespace 分开，旧 key/目录必须迁移或保留。

媒体解析分别找 enclosure 音频、HTML 媒体、站点 canonical URL；图片不能盖掉音频候选。切主题不销毁播放状态。iframe/webview 尺寸须在容器实际计算；Electron webview 的 display/layout 契约勿用通用播放器 CSS 覆盖。登录/认证交给用户与受支持浏览器路径，不绕过第三方限制。

慢启动区分网络、解析、CPU 初始化和渲染；测实际耗时再优化，有超时和退化。离线资产不是“零初始化成本”。移除主题迁移旧选择，不重置全用户设置。输出 PDF/笔记/文件后检查目标文件存在、内容与回跳定位；系统打印对话框不是导出成功。

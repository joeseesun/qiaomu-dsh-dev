# 近期乔木 DSH 项目取证案例

下表是保留的 2026-09-30 历史样本，不是 DSH 永久契约。RSS 本地 HEAD 为 `264124b`，当时比公开 `main` 超前 3 个提交，**不能把本地代码链接为已公开**；Home `2850360`、Radio `5172432` 可在公开仓库核对；Reader 是无 Git 元数据的本地快照。Radio 工作树有未提交文档/构建脚本改动，这里不宣称那些改动已公开。

| 样本 | 代码证据 | 抽象规则 | 验证缺口/反例 |
| --- | --- | --- | --- |
| [乔木 RSS 公开仓库](https://github.com/joeseesun/qiaomu-rss-dsh)；本地未公开快照 `264124b` | `src/host/service.js` 提供 Remote；`src/client/index.jsx` 先 `$mount` 再 `ctx.inject(['remote.rss'])`；`build.mjs` 构建 host/client；`tests/render.mjs` 模拟缺注入报错 | Host 工具注册、Remote namespace 和 Client 面板是三条独立链路 | 旧现场曾出现工具可用但面板不可用；本地代码不能当作公开仓库当前内容 |
| RSS 伴读 | `src/client/native-chat.js` 检查 workspace/草稿/附件并 retain/release；`src/host/article-context.js` 限上下文；`tests/companion-draft.mjs` 断言选文不进入草稿且组件不重挂 | 上下文身份、草稿和原生会话生命周期需独立测试 | 单篇正确回答不证明跨文章可靠 |
| RSS 数据 | `src/host/store.js` 在 DSH home 存 JSON，串行临时文件+rename，dispose 时 flush；`src/host/sanitize.js` 清理文章 HTML | 明确数据 owner、持久化与外部内容边界 | 多进程写冲突仍需单独设计 |
| [乔木 Home](https://github.com/joeseesun/qiaomu-home-dsh/tree/2850360) | `src/client/index.jsx` 通过 slot 注入页面/侧栏；`src/client/store.js` 用 localStorage；`scripts/build.mjs` 生成 client 外壳；`src/client/page.jsx` 壁纸控件层级修复 | UI 命中层级要做真实点击；安装副本和源码要比对 | 当次修复只有测试/构建和安装文件同步，未证明重启后的实际点击 |
| [乔木电台](https://github.com/joeseesun/qiaomu-radio-dsh/tree/5172432) | `src/client/plugin.ts` 通过 slot 挂侧栏/panel；`scripts/build.mjs` 联合构建播放器/Host/Client；`src/client/player.ts` 区分播放失败与取消 | 预览页、Host 路由、Client panel、音频播放分别验收 | 媒体权限和直播流随环境变化 |
| 乔木 Reader 本地快照 | `src/host/index.js` 用原子写与路径边界，`src/client/index.js` 注册面板与退化 UI，`scripts/build.mjs` 包客户端 | 文件类插件特别关注路径、并发、加载失败与 profile 启动 | 无公开 commit 引用，先作为内部案例；不能拿来证明发布状态 |

经验来源是具体代码和已观察到的故障。新插件应先查当前 DSH 官方文档与安装版，而不是复制这些项目的 `inject` 名称、预设尺寸、服务协议或暂时性的兼容写法。


## 2026-10-01 增量复盘

以下从近期聊天的明确结果与测试报告提炼，状态是当时观察，不代表现在每个仓库的实时状态。

| 触发/现象 | 机制与修正 | 新插件回归场景 |
| --- | --- | --- |
| Reader 启动阻塞整宿主 | locale 访问未声明依赖，修正并复测宿主启动 | 必需服务缺失/恢复，其他插件能启动 |
| Radio 长 loading | 本地模型读取快，但 CPU 表面初始化慢；测量后减少计算并加超时 | 首次加载时间、超时、取消、二次打开 |
| Home 换壁纸按钮无响应 | 滚动层拦截点击，修层级 | 实际 pointer hit-test、键盘、遮罩 |
| Home 重置/改名/Tab迁移 | 配置与内容分离，保留 Todo/笔记和旧 key | 有旧内容升级，重置不丢数据 |
| Reader 书库封面全占位 | EPUB可解析封面但目录没传递，接通索引到UI | import→manifest→Host→UI整个数据链 |
| Reader 分页漏下一页文字 | 裁切/页边距与resize定位不一致 | 单页/双页/分屏拖动/搜索回跳 |
| RSS 选段问“翻译”扩成全文 | 区分处理对象与背景；引用在composer内预览 | 两种文章、移除选段、全文要求、已有草稿 |
| RSS 频道空白需手动刷新 | 切频道只读缓存，没有拉取 | 缓存先显、自动加载、并发切换与迟到响应 |
| RSS 音频附件丢失 | 封面图片被当首个enclosure，盖住音频 | 同条目同时有封面+音频+站点链接 |
| RSS webview只显示半屏 | 通用CSS覆盖Electron webview布局 | 目标Electron真实computed尺寸和比例 |
| Podscribe成功抓大文本 | 全文阅读与模型输入预算不同 | 阅读保全文；AI上下文分块/上限透明 |
| 插件改名后依赖/数据不齐 | 包/row/factory/仓库同步；storage namespace保留 | 旧安装升级，不移动内容，不留断路径 |
| 新皮肤重建播放器 | UI外观与播放owner分开 | 播放中切主题、面板关闭、重开及卸载 |
| 图文README来自本地新构建 | 截图需要注明来源，不能证明旧Release | caption含build/version，Release包重新验收 |
| 发布仅合并源码 | tgz+SHA256+公开回读+新profile补完整 | 从公开包开始安装，无开发目录依赖 |

最新 RSS 发布聊天报告 v0.6.0 已公开回读与二次干净安装；Reader最新主题更新仍在进行。不会将进行中的发布/验收写成规则的成功证据。早期缺口在后续记录补齐时，以带时间的新记录为准，不用历史待验收状态否定后来结果。

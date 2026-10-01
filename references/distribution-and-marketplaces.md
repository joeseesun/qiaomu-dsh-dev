# DSH 插件分发与市场提交

核验日期：2026-09-30。以下入口、门槛和文件格式是当日证据，不是永久规则；实际投稿前重读目标站提交页与 contributing。优先官方/市场维护者原文，不采信第三方自称“官方市场”。

## 1. 官方发现与独立市场

DeepSeek 官网“社区插件”指向 GitHub `dsh-plugin` Topics；官方 README 要求作者添加该 topic。未发现独立官方上架审核表单。官方核心插件列表、社区发现、社区精选收录不能混称“官方认证”。

发布请求下，为实际插件仓库增量添加 topics（保留已有标签）：

```sh
gh repo edit OWNER/REPO --add-topic dsh-plugin --add-topic deepseek-harness
# 另选 1–3 个真实能力标签，例如 radio / rss / reading；不堆无关热词。
gh repo view OWNER/REPO --json repositoryTopics
```

GitHub topic 与 package.json keywords 是两套数据。只有 public GitHub topic 能供依赖它的目录扫描；包 keywords 不能替代它。添加标签只证明可发现，不证明已收录。

## 2. 可安装发布包先于投稿

- package.json 声明 dsh.bundle.patch，patch 路径存在并引用正确包名；只有 dsh.client 不构成可安装 bundle。
- 核对 name/version/license/repository/description/files/exports；npm 发布必须移除 private:true，scoped 公开包配置 publishConfig.access=public。不在未验证账号/包名权限前承诺 npm 可用。
- 构建后逐项检查 exports 中 JS 与 .d.ts 真正存在；声明生成失败必须失败退出，不能打印 warning 后继续发布。
- prepack 构建并检查产物；检查 tgz 里 host、client、页面、CSS、HLS/模型等离线资产。不要只看源码目录，更不要依靠本机 node_modules 链接。
- 官方说明 GitHub 源码安装有 prepare 与 pnpm 构建许可问题；不能把缺 lib 且无 prepare 的仓库标成可直接安装。优先 npm 预构建包或 GitHub Release 的 tgz；二者安装无需运行源码构建。
- README 安装命令须与真正交付的渠道一致。npm 未发就写未发；Release tgz 下载后使用 dsh plugin --profile <已有 web/desktop profile> add ./package.tgz，profile 不硬编码用户本机名字。
- 独立 DSH_HOME/profile 做安装，不改日用 profile：验证包不是开发目录 symlink，dump-config 有 bundle，启动目标宿主，页面/资产可读，client 入口和目标动作正常。记录 DSH 版本、精确 commit、包 SHA256、平台。模拟 host 的 HTTP 测试不能冒充完整 DSH 启动。
- 从已发布 URL 下载到新目录再比对摘要/安装，避免只验证上传前本地包。源码合并、CI、Release、下载、干净安装、界面、目录上架逐项报告。

## 3. Awesome DSH Plugin 与 dsh-market

维护者指南：https://github.com/awesome-dsh-plugin/awesome-dsh-plugin/blob/main/contributing.md

一个插件提交一个文件 `data/plugins/<owner>__<repo>.yml`：

```yaml
url: https://github.com/owner/repo
name: owner/repo
category: fun
description:
  en: Listen to live radio inside DeepSeek Harness.
  zh: 在 DeepSeek Harness 中收听直播电台。
```

- description.en 必填；中文可选；功能描述应与代码相符，不能用营销词或虚构数量。含冒号加空格的 YAML 文本加引号。
- 必须有 dsh.bundle、真实工作代码、dsh-plugin topic、活跃公开仓库；当日规则要求仓库创建满 1 天，没有提交次数门槛。通过 GitHub created_at 算满 24 小时的时刻，不能按跨自然日计算。
- 每 PR 最多 3 条；优先一条一个 PR。README 自动生成，不要手工改。CI 通过仍需维护者阅读和审核，不等于录用。
- category 按实际功能选，电台属 fun；播放器内部多皮肤不等于替换 Harness 全局主题，不能因此塞进 theme。
- `screenshots.json` 放在自己仓库 package.json 旁，列 1–8 张仓库相对图片路径。不得越界，第三方图床不支持；截图不得含用户私人会话、账号、token。真实预览截图优先。
- npm 可选；如发布，package.json.repository 指向收录仓库，目录会自动关联；不要擅自添加 npm: YAML 字段。
- dsh-market 使用该目录的数据，向目录提交，而不是向市场应用仓库 PR。合并后等待同步并实际查询详情页/安装结果，不承诺固定审核时限。

## 4. 其他独立社区入口

| 入口 | 方式 | 边界 |
| --- | --- | --- |
| https://dshmarketplace.dev/submit | 填 public GitHub URL；也声明扫描 dsh-plugin；精选目录另走其 data/curated.yml PR | 与 Awesome 是两个项目，勿把文件格式混用；表单人工审核 |
| https://dshplugin.app/submit | GitHub URL 必填；邮箱/备注可选，无账号要求 | 审核与公开条目分开；安全验证需按工具政策处理 |
| https://dsh-plugin.org/zh/submit | topic 扫描；README 有安装/profile/许可/权限/兼容证据 | 社区项目，不是官方认证；页面收录不保证兼容 |

不要向所有叫 DSH Market 的域名盲投。先确认运营方、投稿入口、真实数据源，去重共享目录。研究请求不提交；用户授权发布/投稿后才操作。满一天门槛未到时准备好条目并报告最早时间，只有用户要求后续自动提交才安排自动化。

## 5. 可复用交付清单

- 公开仓库 + topics 回读 + 许可证 + 中英文一句话描述。
- 与发布包一致的 README、安装/profile、兼容版本、隐私/网络与卸载说明。
- 真实无私人信息的截图、screenshots.json、版本化 Release/tgz 或 npm。
- exports/打包/独立安装/宿主用户路径的证据。
- 目录 YAML 或表单资料就绪，分别记录 submitted / accepted / visible / install verified。

## 来源与漂移

- 官方官网社区入口：https://deepseek.com/harness/
- 官方 README：https://github.com/deepseek-ai/deepseek-harness#community-and-support
- 官方分发文档：https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md
- Awesome 投稿：https://github.com/awesome-dsh-plugin/awesome-dsh-plugin/blob/main/contributing.md
- dsh-market 数据源：https://github.com/dsh-market/dsh-market#submit-your-plugin
- 上表每个市场自己的提交页。

乔木电台案例（2026-09-30）：本地 link 安装能运行，但公开仓库无 Topics/Release，private:true 阻止 npm 发布，exports 的声明路径与真实输出不一致。经验是检查消费端产物，不能由本机可用推断公开可安装。这是案例，不把当时包名、版本、皮肤数或等待时间写成通用要求。

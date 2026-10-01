# 自包含发布流程

不依赖其他 skill。按已授权渠道发布；长期发布授权继续有效。仅研究/审查不推送。命令参数依项目与当前 CLI 替换，禁止把文档占位符原样执行。

## A. 固定候选版本

查看 git status、branch、remote、已发 tag、并行开发。保留已有改动；候选 commit 必须包括待发布完整功能，不能安装混合半成品。通过 feature branch → PR → CI → merge 管理。改动不在远端源码树时先用独立 clone/worktree 对照 diff，避免覆盖远端 README、截图、合法文件和发布检查。

保留项目许可证；从 GPL 产品迁移的代码不能因为 skill 自身 MIT 就改成 MIT。打包清单不带用户数据、local profile、token、临时诊断或大日志。新功能升版本，不覆写既有 tag/Release。

## B. 可消费产物

运行项目已有 check/typecheck/test/build，再 pack；使用 `npm pack --json` 或项目等价命令获取精确 tgz 文件，不根据 name 猜 filename。`prepack` 失败必须停止。

```bash
python3 /path/to/skill/scripts/dsh_dev.py audit /path/to/package.tgz
```

检查 exports/main/types、patch 列表、icon/locale、client chunks、CSS、EPUB/媒体等资产。audit 静态检查不能解析 Loader 完整 YAML 或证明源码/服务语义。用真正 dump-config 补充。`private:true` 阻止 npm 发布，但可交付预构建 Release tgz，不能一概报包不可用。

## C. 独立安装与宿主验收

查 CLI help；以临时 DSH_HOME，从官方 web 模板初始化**含 Web surface**的测试 profile。仅 plugin add 的 base-backed profile 不保证 GUI。示意（需当前 CLI 验证）：

```bash
DSH_HOME=/tmp/dsh-test-home /absolute/dsh --profile plugin-qa --from-default-profile web --dump-config
DSH_HOME=/tmp/dsh-test-home /absolute/dsh plugin --profile plugin-qa add /absolute/package.tgz
DSH_HOME=/tmp/dsh-test-home /absolute/dsh --profile plugin-qa --dump-config
DSH_HOME=/tmp/dsh-test-home /absolute/dsh --profile plugin-qa --no-open
```

Desktop 使用其 bundled CLI 和 initialized desktop profile，不能用全局 CLI 覆盖 reserved profile。优先在另一个测试运行环境验收；日用更新按用户已授权范围执行。先备份数据与配置，核对当前 session 是否正在使用，避免两个聊天同时重启。

安装 manager 的 application/warnings 决定 applied、overridden、failed、restart-required；安装路径/摘要/版本单独核对。重载后走用户路径，检查 locale、主题、键盘、选文、工具、媒体与卸载。模拟宿主和 HTML 样机只证明组件。

## D. GitHub 与公开渠道

`gh auth status` 与 repo 权限只检查必要信息，不输出 token。README 按包实际安装渠道写；添加 dsh-plugin topic 后回读。PR 用 body-file 保留换行，创建后 attach_artifact（所在工具可用时）。检查所有 required checks、review、mergeability，不能以本地测试替代远端 CI；未通过则修复，不合并。

合并后核对 default branch commit 与候选包源码；如 merge 改代码，重建并再验收受影响路径。Release 附 tgz、SHA256SUMS、changelog、兼容与验收范围。npm 仅在账号/包权限、access 和 private 检查通过且获得该渠道授权后发。

从**公开 URL**下载到空目录，用可信候选摘要验证：

```bash
python3 scripts/dsh_dev.py verify-download --url PUBLIC_TGZ_URL --sha256 CANDIDATE_SHA256 --output /tmp/public-plugin.tgz
```

再用下载的包在第二个独立 profile 安装/启动/打开目标入口。公开下载可验证≠运行功能证明。网络无公开渠道时明确缺证。

## E. 社区发现与恢复

读取 [市场指南](distribution-and-marketplaces.md)，当天刷新运营方规则与数据源。topic discoverable、提交、被录用、市场可见、安装成功分别记录；Awesome 等社区不是官方认证。没有投稿授权时只准备条目。不可用渠道不阻止已验证渠道交付。

回滚用前一个已验证 tgz 安装，并恢复备份配置；涉及数据迁移先核对旧版本能否读新数据。移除 bundle 不默认删除插件数据。失败时保留日志、候选 hash 与清晰恢复动作。

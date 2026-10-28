# v0.3.0 宿主兼容能力验收

日期：2026-10-28。平台：macOS；Node 24.21.0；Python 3.14.7。本文只记录已执行的检查。

- `python3 -m unittest discover -s tests -v`：18 项通过，包括同版本同长度旧字节、缺资源、symlink 越界、恶意归档和声明优先级元数据。
- skill-creator `quick_validate.py`：通过；维护用 PyYAML 位于临时 venv，自带命令不依赖 PyYAML。
- skill-publisher dry-run：结构、README、既有作者资产检查通过，未建立本地独立安装副本。
- npm 固定 `dsh-plugin-health@0.5.0`，按本 skill 配方隔离安装，未装入日用 DSH。
- 实际静态矩阵：RSS 公开 v0.8.0 与 v0.9.1 × 宿主 0.2.1-rc.2/rc.3。旧包两列不兼容，新包两列兼容；`--fail-on any` 返回 1，符合预期。这里只证明声明。
- 实际官方 npm DSH 0.2.1-rc.3 + RSS v0.9.1 公开 tgz：health smoke 原生安装、启动、`rss_list_channels` 注册及真实调用、关闭全部通过。未调用模型或执行外发。
- 反例：同一包断言不存在的 `missing_qiaomu_acceptance_tool`，安装成功但 assertions 阶段失败，退出 1；没有把安装成功视为功能通过。
- 新 `compare-install` 命令：公开封面 v0.1.1 安装副本 11 个打包文件全部一致；此前同版本缓存副本检测到 `client.js` 内容不同，退出 1。没有改动这些副本。

## 范围

兼容流程与 CLI 配方已整合；CI 模板只提供静态声明检查。未在各产品开启定时任务、无人值守修复或自动发布。health 的 UI、repair、市场索引没有作为本轮已验收功能。Windows/Linux 实际宿主与 rc2 运行时未验证；rc2 的矩阵通过不是 rc2 功能验收。

第三方工具来源：[EasonMWS/dsh-plugin-health 固定源码](https://github.com/EasonMWS/dsh-plugin-health/tree/91deca87cad7de17711b88ffa2c6b2f785ee4e6b)。npm 0.5.0 integrity：`sha512-bPNSv02OzSkcCZNHlnBqcYEuvSr9z1Jl19OSz9dfXmkTi5KUjfNfUfAlRvAzmhsN1OAJ6QBTUksTo29W73Eoaw==`。

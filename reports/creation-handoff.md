# 创建交付（2026-09-30）

**结果**：`qiaomu-dsh-dev` v0.1.0，指导持久化 DSH 插件从当前 API 取证到真实运行与公开安装。唯一源目录为个人 `.agents/skills/qiaomu-dsh-dev`。

**参考学习**：官方 `cordis-plugin-development` 的当前宿主检查；NanmiCoder `dsh-plugin-development` 的 Host/Client 与 profile 分层；乔木 Obsidian 开发 Skill 的按需参考和宿主验收；`codebase-design` 的明确接口选择。来源、固定版本和取舍见 `reports/prior-art-research.md`。

**取舍**：保留版本取证与真实用户路径；把案例收窄为可验证故障，不将 RSS/Reader 的当前服务名推广为 DSH 常量；舍弃动态 Cordis Run 的安装与审批流程。原创的五层证据矩阵连接 RSS 的 Remote 问题、Home 的安装副本与点击问题、Radio 的客户端外壳、Reader 的文件可靠性。

**优势与证据**：

- [design advantage] 根文件保持路由与最短流程，四个按需参考分别覆盖架构、数据/UI、验证、案例；对应文件可直接检查。
- [validated advantage] 触发案例与包验证结果以生成的 `reports/trigger-eval.json`、`reports/skill-ir.json` 和本地检查日志为准。
- [hypothesis] 五层证据矩阵可能减少“源码完成=用户可用”的误判；尚缺新项目端到端或对照评测。

**边界**：Skill 不替代官方当前 API、安装过程或实际 GUI 验收；不包含本机凭据、profile 数据或私有源码。发布后的全新安装和真实 DSH 开发案例须分别核实。

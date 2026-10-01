# 0.2.0 本地验证 · 2026-10-01

- 标准库Python脚本：系统Python 3.9.6运行，13项unittest通过（含原有2项契约检查）。
- 触发启发式评测：27/27，0误触发/0漏触发；不是LLM行为评测。
- Skill IR、manifest与frontmatter统一0.2.0，结构检查通过。维护工具需PyYAML，使用已装Python 3.14.7；用户运行dsh_dev.py无需PyYAML。
- 三张README SVG的XML解析通过，相对路径存在。
- 实际脚手架：无依赖Host bundle打包成功，tgz审计通过；独立DSH_HOME/web模板profile用Desktop bundled CLI 0.2.0-rc.2安装；dump-config出现插件row；启动日志出现QIAOMU_DSH_SKILL_SCAFFOLD_ACTIVATED，Host启动成功。测试进程已停止，没有修改日用profile。
- 同版本重复打包再次安装被pnpm判断up-to-date；测试候选升0.1.1后确认新artifact激活。此故障强化不可复用发布版本的规则。
- 公开下载工具对RSS v0.6.0实际Release tgz匿名下载、摘要和包审计通过；hash 711f5b9d058c5735760859ce9a2a938085de477999974556ed6110a5df4da256。这里仅验证工具，不声称本轮重测RSS功能。
- 安全扫描通过；无用户profile、原始聊天或凭据被打包。

限制：Host脚手架不包含业务能力；未用新版skill完成复杂Client插件的独立Agent任务、跨平台运行或同题对照。Nowledge历史检索服务连接被拒绝，15聊天复盘不代表全历史完整覆盖。

公开PR/Release/隔离Skill安装由发布器执行，结果见发布产物，不预先声称已发布。

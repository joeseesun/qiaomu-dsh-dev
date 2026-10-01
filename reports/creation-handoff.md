# qiaomu-dsh-dev 0.2.0 交付

更新于 2026-10-01。唯一源为个人 canonical skills 目录；参考、脚本、模板、工程图均随包安装。

实际研究的参考skills：官方 persistent cordis-plugin-development，dsh-client-ui-ux，dsh-code-review，dsh-pre-push-checks，dsh-find-simplifications；Pilot的dynamic cordis-plugin-development与editing-cordis-compositions。候选具体取舍见 research-20261001.md。社区SSH/Remote/Vision是工程机制锚点，不宣称质量排名。

**设计优势**：按Context与Service边界选实现，少依赖内部Client包；UI/Tool共用Host operation；一包覆盖开发、README、验收和发布。

**已验证优势**：标准库脚本有消费端失败回归；init脚手架经npm pack、独立DSH 0.2.0-rc.2 profile安装、dump-config和Host apply激活，验收日志有明确marker。它是最小Host脚手架验证，未证明复杂业务或Client交互。

**假设**：会缩短复杂插件开发与发布时间。未做同题Agent对照/跨平台完整运行或满意度调查。

拒绝：照抄动态代码环境禁import到编译插件、把旧API目录写死、重复手动改用户profile、把安装量当质量、把HTML样机当实机截图、强行用内部DOM桥接原生composer。

包级验证与公开发布结果在 validation-20261001.md 和自动发布报告；缺证仍单独保留。研究原始聊天与profile凭据未打包。

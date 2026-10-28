# 宿主升级与兼容演进

用于「升级 DSH 后插件失效」「批量适配新版本」「接入兼容 CI」。先确定目标宿主、用户实际安装包、候选源码与核心动作；普通功能开发不必运行完整版本矩阵。

## 采用哪些机制

| 来源 | 在本 skill 中的用途 | 证据边界 |
| --- | --- | --- |
| [DSH rc3 官方评估器](https://github.com/deepseek-ai/deepseek-harness/blob/dsh-v0.2.1-rc.3/packages/boot/app-boot/src/plugin-compatibility.ts) | 目标版本的兼容声明依据 | 声明接受不证明 API 和业务行为正确 |
| [EasonMWS/dsh-plugin-health](https://github.com/EasonMWS/dsh-plugin-health/tree/91deca87cad7de17711b88ffa2c6b2f785ee4e6b) | 可选 CLI：matrix、隔离 profile smoke、只读 doctor | 浏览器专属插件仍要 Web/Desktop 验收；不自动修源码 |
| [PerryLink/dsh-plugin-upgrade](https://github.com/PerryLink/dsh-plugin-upgrade) | 借鉴旧 API 扫描、变更清单与迁移映射 | 其公开指南针对较早固定版本段，不能充当 rc3 通用 codemod |
| [ZK-Andy/dsh-continual-evolve](https://github.com/ZK-Andy/dsh-continual-evolve) | 借鉴「证据 → 提案 → 验证 → 可回退变更」 | 主要面向记忆和 skills，不是插件源码自动升级器 |

来源核对：2026-10-28；health npm **0.5.0**。本包集成工作方法和调用配方，不复制第三方实现。health 是可选依赖，不要求安装到用户日用 profile；缺少它时仍可用目标官方 CLI/评估器完成检查。新版本先刷新官方实现与工具帮助，不能把本节 rc3 规则永久套用。

## 先复现真实发布包

1. 记录宿主精确版本、平台、安装器来源；读取公开 tgz 的 package.json，再与 main/candidate 对照。用户使用旧 Release 时，只测 main 会漏掉故障。
2. 用本包 `audit` 查看包中声明和结构。`compatibility_declarations.evaluated` 恒为 false；它只展示原始元数据，不执行 semver，也不证明兼容。
3. **rc3 规则**：存在 `engines.dsh` 时只评估该字段；仅缺失时才检查所有 `@deepseek-ai/dsh` / `@deepseek-ai/dsh-*` peers。无效或空 engine 不是“缺失”。使用 `includePrerelease:true`；workspace 范围依官方规则展开。不能只看到旧 peer 就断言拒装。
4. 版本豁免是特定包版本与宿主组合的放行，不是修复。不要把 `allow-version` 或矩阵 exemptions 当作发布通过条件。
5. 为新版本声明支持范围前检查真实契约与行为；声明过窄可能误拒绝，范围过宽又不能提供未来兼容保证。保留已有支持需有依据，未复测的旧版本单独标注。

## 可选 health CLI：固定工具版本，隔离安装

以下命令在任务临时目录执行，替换实际路径；这些操作是显式安装工具，不是 skill 加载时的隐式动作。依赖锁文件、Node/pnpm 版本与工具版本一并记录；固定顶层版本不等于所有传递依赖永不变化。

```bash
qa_dir=$(mktemp -d)
npm install --prefix "$qa_dir/tools" --ignore-scripts --no-audit --no-fund dsh-plugin-health@0.5.0
health_cli="$qa_dir/tools/node_modules/.bin/dsh-plugin-health"
"$health_cli" --version
"$health_cli" --help
```

`--ignore-scripts` 适用于已核验的 health 0.5.0 CLI 安装，不应直接套用到需要原生模块的 DSH 或产品构建。第三方代码按其许可证使用，审查新的 CLI/workflow 版本后再升级；不要默认跟随 main 执行有发布权限的工作流。

### 声明矩阵

```bash
"$health_cli" matrix \
  --plugins /absolute/plugin-repo \
  --versions 0.2.1-rc.2,0.2.1-rc.3 \
  --out "$qa_dir/candidate-matrix" --fail-on any
```

health 0.5.0 的 `--plugins` 接受目录、npm spec 或文本清单，**不直接接受 tgz**。检查发布包时先 `audit`，然后只读取该包的 manifest 到一个新目录：

```bash
mkdir "$qa_dir/published-manifest"
tar -xOf /absolute/plugin.tgz package/package.json > "$qa_dir/published-manifest/package.json"
"$health_cli" matrix \
  --plugins "$qa_dir/published-manifest" \
  --versions 0.2.1-rc.3 \
  --out "$qa_dir/published-matrix" --fail-on any
```

这是静态 manifest 检查，不执行包代码。正式验收固定明确宿主版本；`latest/next/alpha` 仅用于发现新版本，解析后保存精确版本再建立发布证据。矩阵报错和不兼容都应使 gate 失败；只读扫描不擅自修复用户 profile。

### 原生安装、启动与真实工具调用

安装官方目标宿主到隔离目录，或提供已安装、可由当前 Node 解析且导出 `profile-boot` 的 `@deepseek-ai/dsh` 包目录。macOS Electron 的 app.asar 路径不等于普通 Node 可读的 npm 目录；Desktop bundled CLI 的真实 UI 验收仍按发布手册执行。

```bash
npm install --prefix "$qa_dir/host" --no-audit --no-fund @deepseek-ai/dsh@0.2.1-rc.3
"$health_cli" smoke \
  --dsh-dir "$qa_dir/host/node_modules/@deepseek-ai/dsh" \
  --plugin /absolute/plugin.tgz \
  --tool actual_tool_name --calls /absolute/smoke-calls.json \
  --install-timeout 120000 --timeout 30000 \
  --out "$qa_dir/runtime"
```

将工具名和 calls 文件换成该产品已有的真实协议。调用格式是 `[{"name":"actual_tool_name","arguments":{},"expectedValue":42}]`；expectedValue 比较整个返回 value，只有确定性操作才填写。`--tool` 仅验注册；`--calls` 才执行调用。至少提供一种断言，缺工具的纯 UI 产品走独立 Web/Desktop profile，不能靠省略断言制造通过。

选择只读或临时测试数据的操作；有外部副作用、模型费用或凭证的路径按任务授权另验。临时 DSH_HOME 隔离数据，不隔离 OS 权限。smoke 检查启动、断言、关闭，任何阶段失败或超时都保留失败结果及日志；不要增大超时来掩盖死锁。报告可能含环境细节，分享前只保留必要诊断。

### 只读安装诊断

```bash
"$health_cli" doctor --home /absolute/test-dsh-home --profile plugin-qa --runtime 0.2.1-rc.3
```

doctor 可辅助解释缺包、声明冲突、残留配置与 profile 漂移。repair 的隔离文件/改 patch 功能不是源码适配；普通兼容任务不自动执行 repair。确需修安装状态时，先看 dry-run 和数据备份，在已有授权的明确目标内操作。

## 核对安装副本，避免验错包

同路径、同版本 tgz 重打后再次 add，可能继续使用旧的已安装文件。候选包采用带摘要的唯一测试路径和全新 profile；安装后检查：

```bash
python3 scripts/dsh_dev.py compare-install /absolute/plugin.tgz \
  --installed /absolute/test-profile/node_modules/package-name
```

传的是具体包目录，作用域包如 `node_modules/@scope/name`。命令逐个比较打包文件，检测缺失、旧字节与外部 symlink，不修改安装目录；不检查额外文件，也不证明进程已重新加载。实际页面显示版本应来自产品 package.json；不要误改数据格式版本或上游历史记录。

## 从一次修复到跨产品维护

维护一份现有产品清单，包含仓库、公开资产、宿主范围、check 命令、核心动作和回滚路径；不要默认给各产品新装监控插件。

- **发现**：用户需要持续监控时才新增定时触发；去重官方版本与 commit。手动维护也走相同流程。
- **诊断**：矩阵 → 正常安装 → 启动/工具 → 产品 UI；区分声明拒绝、API 变化、安装缓存、服务注入和业务失败。
- **适配**：只修已定位的层。原始错误、上游变更与最小复现进入 PR；同一原因两次修复尝试仍失败时保留证据，先重新定位，不无限循环改范围。
- **放行**：已有产品 check、目标宿主验收、PR/CI、公开资产与第二次独立安装都通过。未知 API 变化和数据迁移不能因为矩阵绿灯自动发布。既有发布授权继续有效；新增无人值守调度另按任务范围实施。
- **沉淀**：经实测确认的通用契约更新到本参考；产品特有问题留在项目文档。保留前一稳定包；回滚数据需验证旧版本可读，不能只退代码。

[静态 CI 模板](../templates/dsh-compat.yml) 可复制进产品仓库。默认 read-only token、明确宿主版本、无定时器/自动改码/发布；它只增加声明门槛，不能替代 runtime 和 UI。不要直接照抄上游可复用 workflow：核对 toolVersion、failOn（不能是 none）、权限及输入拼接方式。

产品专属路径例：RSS 全文/伴读草稿，Reader EPUB/进度/笔记，Home 待办/provider，Radio 目录/可控音频源，UI Learn 词典/记录，Cover 模板/撤销/导出，Audio 保存/TTS，Publish 本地排版，Blog Publisher 测试站点发布。外发用测试端点，禁止用自动化操作用户微信客户端或微信内嵌页面。

完整发布步骤见 [release-runbook.md](release-runbook.md)；验收记录使用 [ACCEPTANCE.md](../templates/ACCEPTANCE.md)。

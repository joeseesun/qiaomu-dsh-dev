---
name: qiaomu-dsh-dev
description: |
  Develop, debug, review, test, install and release persistent DeepSeek Harness (DSH) Cordis plugins and bundles. Use for host services/tools, client slots/panels, Remote bridges, native conversations, plugin data, package/profile integration, build failures, UI regressions and live-host verification. Check the installed Harness version and current API before applying examples. Exclude Obsidian-only plugins, generic web apps, one-off DSH usage questions, dynamic Cordis-run packages and skill authoring.
metadata:
  author: 向阳乔木
  version: "0.1.0"
---

# 乔木 DSH 插件开发

面向**持久化、可安装的 DSH 插件**。目标是把用户动作从源码一直验证到实际运行的宿主；注册成功、构建成功、界面可见、功能可用和公开可安装是不同证据。

用户指令与项目 `AGENTS.md` 优先。只读诊断保持只读；开发请求完成实现与测试；只有明确要求发布时才改 GitHub/Release。保护当前 profile、用户数据和其他插件，优先在独立测试 profile 验证。不要把本技能中的历史代码路径或版本当成当前 DSH API。

## 路由

1. 确认仓库、分支、改动、目标 DSH 版本、运行 profile、已安装包与实际入口；保留用户已有改动。按用户结果选择 **host**（工具、文件、网络、持久化）、**client**（slot、页面、交互）或双端。纯 host 不创建 client。
2. 先查当前版本的官方文档、已安装包 `exports`/类型/源码和可用的 `cordis_inspect`；只读审查不改 profile。按需读 [架构与契约](references/architecture.md)。当官方当前契约与本技能案例冲突时，以目标运行版本为准。
3. 画出最短用户路径：动作 → 入口/slot/工具 → 所需服务与 `inject` → Remote/Host 副作用 → 状态/错误反馈 → 卸载/恢复。明确谁持有数据、谁清理资源、缺服务时如何退化。
4. 在现有架构内最小修改。新增文案同时进入语言字典；输入、菜单、快捷操作要保留键盘、焦点、草稿与失败恢复。AI 伴读、外部内容和写入按 [数据与界面](references/data-and-ui.md) 验证。
5. 跑项目已有 lint/typecheck/test/build，再核对构建产物、`exports`、`files`、bundle patch 与 profile 组合。安装/更新到**明确的测试 profile**，重载/重启后走真实用户路径；按 [验证与发布](references/verification.md) 记录每层证据。
6. 若是故障，先复现并定位哪一层失效，修复后复测原场景和一个邻近场景。按需读 [四个乔木项目案例](references/cases.md)，其中记录的是样本经验而非框架保证。

## 关键判断

- Cordis `inject` 是运行依赖；`dsh.client.inject` 是包元数据，二者用途不同。不能因为 host 工具已注册，就认定 client 的 `remote.*`、slot 或面板可用。
- 客户端构建形式由**当前目标宿主**决定。最近乔木项目使用 `window.__ModuleLoader__.load({ id, factory(require) })` 的 CJS 外壳；必须核实目标版本的加载器及可外部化模块，不能照搬旧清单或把浏览器代码打成裸 ESM。
- Bundle 是分发层，profile 是运行组合。核对安装副本与源码摘要、配置覆盖顺序、必需依赖和实际启动日志。修改源码不会自动更新 `file:` 安装副本或已加载模块。
- 只在真实运行面证明用户可见行为：图片、媒体、网络、原生会话、选文、导入导出都要测试成功、失败及状态恢复。自动化冒烟测试是前置证据。
- 公开发布分别核对 PR、CI、合并、Release/包、全新 profile 安装与实际界面；不得由前一层推断后一层。

## 输出合同

交付：触发条件与根因；改动文件及用户可见效果；测试命令与结果；源码/产物/profile/真实界面各层状态；数据迁移与回滚注意点；未覆盖的 DSH 版本或平台；公开发布的精确阶段。需要用户测试时给出最短动作和可观察结果。

版权所有 (c) 向阳乔木 · [X](https://x.com/vista8) · [GitHub](https://github.com/joeseesun/)

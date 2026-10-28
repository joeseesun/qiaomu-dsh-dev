# 发布候选验收

- Plugin/version/commit：
- DSH version/runtime source/platform：
- 测试 profile 与数据来源（无凭据）：
- 候选包 filename/SHA256：
- 升级任务：旧公开包版本/hash、目标宿主矩阵、health/官方评估器版本：

| 层 | 状态 passed / failed / pending / not applicable | 证据与限制 |
| --- | --- | --- |
| 源码与现有改动保护 | pending | |
| typecheck/test/build | pending | |
| tgz exports/patch/assets | pending | |
| 声明矩阵（公开包/候选） | pending | 静态结果不能证明运行 |
| dump-config与安装副本逐文件比对 | pending | |
| 原生 smoke：注册/实际调用/关闭 | pending | 不适用于纯 UI 时注明 |
| 启动与Client materialization | pending | |
| 用户成功/失败/恢复路径 | pending | |
| 停用/重启用/卸载 | pending | |
| locale/theme/keyboard/narrow | pending | |
| 数据迁移与回滚 | pending | |
| README真实图与命令 | pending | |
| PR/CI/default commit | pending | |
| Release/公开下载/二次安装 | pending | |
| 市场 submitted/accepted/visible | pending | |

## 用户路径

入口→输入→动作→可观察结果；两种不同材料和已存在草稿的测试（适用时）。

## 复测与限制

最短步骤；未覆盖的版本/平台/模型路径；回滚包与数据备份位置。

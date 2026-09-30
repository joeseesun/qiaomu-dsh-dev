# 先例研究（2026-09-30）

`qiaomu-meta-skill/scripts/research_prior_art.py` 用三组查询检索了 skills.sh 与 SkillsMP，返回 80 个去重候选家族；原始候选在 `reports/prior-art-candidates.json`。skills.sh 的 installs 是安装量，不是评分；SkillsMP 的 stars 是来源仓库指标，不能相加。初次运行误用系统 Python 3.9，`datetime.UTC` 导入失败；改用 Python 3.14 后两目录均返回结果。

| 实际阅读的参考 Skill | 信号与维护 | 吸收机制 | 不采纳 |
| --- | --- | --- | --- |
| [DSH 官方 cordis-plugin-development](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/preset/agent-preset/skills/cordis-plugin-development/SKILL.md) | 官方仓库固定 commit；skills.sh 检索时显示 3 installs，不能据此评质量 | 用当前宿主 inspection/安装结果验证 service、slot 和 profile，而非凭示例猜 API；真实界面是交付边界 | 官方 Skill 聚焦当前 profile 的持久化插件和内建工具，工具名/审批流不能普遍套到外部开发环境 |
| [NanmiCoder dsh-plugin-development](https://github.com/NanmiCoder/dsh-agent-teams/blob/9cba4fe4171f27c019991cafd2a107f87ef3517b/skills/dsh-plugin-development/SKILL.md) | 固定 commit；skills.sh 显示 164 installs；源文档自己提醒旧接口会漂移 | Host/Client、bundle/profile、独立测试组合分层；版本取证优先于复制代码 | 不复制其历史 `dsh-client-runtime` 等接口表或把当前版本兼容断言写死 |
| [乔木 Obsidian 开发 Skill](https://github.com/joeseesun/qiaomu-obsidian-dev)（本地 v1.12.0） | 本机已存在的跨产品工程参考；未核对公开仓库地址/安装指标，链接仅为候选地址 | 按需参考文件、安装边界、真实宿主验收、发布状态分层 | 不移植 Obsidian Vault/Editor/官方插件目录的专用流程 |
| [Matt Pocock codebase-design](https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md) | skills.sh 703.4K installs；仅作采用信号 | 把 Host/Client 和数据 owner 视为明确的接口选择，避免无必要的桥接 | 不引入其完整术语系统或把参考型 Skill 当执行流程 |

**keep**：版本取证、边界划分、真实组合与用户路径验收。**adapt**：将这些机制用于乔木 RSS/Home/Radio/Reader 的双端工程，强调源码→产物→profile→界面→公开安装。**reject**：硬编码旧 DSH 类型/slot/工具名、复制动态 Cordis Run 代码、把安装量当质量。**invent**：用近期四插件的已定位故障构成回归矩阵，特别是 Remote consumer 注入、安装副本漂移、原生草稿与选文、壁纸点击层级。

权威参考另核对 [官方入门](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/) 与 [官方打包教程](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish)。目标安装版本仍需在每次实际开发中核实。

缺证据：没有对参考 Skills 做同题输出对照或真实用户满意度评测；没有以新 Skill 完成独立 DSH 插件项目的端到端验收。

# {{PLUGIN_NAME}}

{{一句话：谁用、做什么、得到什么结果}}

![{{核心用户动作完成后的真实界面}}](docs/screenshots/main.png)

> 截图来源：{{插件版本 / commit / DSH版本 / 平台}}。{{开发构建或发布包，明确验证范围}}

## 安装

前置：{{实测DSH版本}}，{{CLI或Desktop}}。从 [Release]({{真实Release链接}}) 下载预构建 tgz 后：

```bash
dsh plugin --profile YOUR_PROFILE add /absolute/path/ACTUAL_PACKAGE.tgz
```

{{Desktop bundled CLI定位方式、profile选择、重载步骤、在哪打开入口。未发npm就不写npm安装。}}

## 使用

1. {{入口}}
2. {{输入/选择}}
3. {{用户能观察到的完成结果}}

![{{关键设置或第二条路径}}](docs/screenshots/settings.png)

{{图片说明，不重复标题}}

## 功能与兼容

| 能力 | 行为 | 已验收范围 |
| --- | --- | --- |
| {{能力}} | {{可观察行为}} | {{平台/版本/限制}} |

## 配置、隐私与权限

{{本地数据目录策略、外部网络服务、凭据配置、工具副作用、用户专属授权}}

## 升级、卸载与恢复

{{版本迁移与备份步骤}}

```bash
dsh plugin --profile YOUR_PROFILE remove ACTUAL_PACKAGE_NAME
```

{{重载；默认保留哪些数据；失败如何装回前一版本}}

## 排错

{{找不到入口/依赖等待/旧产物/网络失败的最短检查，issues入口}}

## English

{{Value, installation, compatibility, usage, privacy, uninstall and known limitations}}

## Development

{{从干净clone构建、测试、打包的真实命令；贡献方式}}

## License

{{实际许可证与第三方资产归属；未经核实不替换为MIT}}

# 贡献指南（Contributing）

感谢你对 shopingOnline 的关注！欢迎通过以下方式参与贡献。

## 行为准则

参与本项目即表示你同意遵守我们的[行为准则](CODE_OF_CONDUCT.md)。

## 如何贡献

### 报告 Bug

1. 先在 [Issues](https://github.com/leipengic/shopingOnline/issues) 中搜索是否已有人报告相同问题。
2. 提交新 issue 时请包含：
   - 环境信息（操作系统、Python 版本、浏览器及版本、Selenium 版本）；
   - 复现步骤与报错信息；
   - 涉及的商城与操作环节（登录 / 结算 / 提交订单）。

### 提出功能建议

在 issue 中说明功能要解决的问题、使用场景与期望行为。

### 提交代码（Pull Request）

1. Fork 本仓库并克隆到本地；
2. 从 `master` 分支创建功能分支：`git checkout -b feature/xxx`；
3. 保持代码风格一致，测试通过后再提交；
4. 推送并创建 Pull Request，说明改动内容与原因。

## 开发约定

- Python 3.8+，遵循 PEP 8；
- 页面操作优先使用显式等待（WebDriverWait），避免固定 `time.sleep`；
- 选择器改动请在 PR 中说明验证过的浏览器版本；
- 请勿提交任何用于绕过平台安全机制、批量刷单或违反商城规则的代码。

## 免责声明

本项目仅供学习交流，请勿用于商业用途或违反平台规则。

感谢你的贡献！

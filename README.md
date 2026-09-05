# shopingOnline

JD 商城自动抢购脚本（Selenium 实现）：登录 → 等待到点 → 结算 → 提交订单。

> 仅供学习交流，请勿用于商业用途或违反平台规则。

## 特性

- 支持 edge / chrome / firefox 浏览器，命令行参数化配置
- 显式等待（WebDriverWait）替代固定 `time.sleep`，页面元素等待更可靠
- 到点前 5 秒自动进入高频轮询模式（50ms），提高抢购精度
- 完善的日志输出与异常兜底，抢购完成后保留浏览器供付款

## 环境要求

- Python 3.8+
- 本机已安装目标浏览器（Edge / Chrome / Firefox）

```bash
pip install -r requirements.txt
```

## 主要第三方库

本项目只依赖一个第三方库，其余全部使用 Python 标准库。

### 浏览器自动化

| 库 | 在项目中做的事 | 为什么选它 |
|---|---|---|
| `selenium` | 驱动 Edge/Chrome/Firefox 打开商城首页与购物车，执行登录、全选、去结算、提交订单等点击操作；配合 `WebDriverWait` 做显式等待 | 抢购必须跑在真实浏览器里（登录态、Cookie、前端交互缺一不可），而 Selenium 的 WebDriver 协议是行业标准，三种浏览器一套代码通用 |

### 标准库承担的部分

- `argparse`：命令行参数（浏览器、抢购时间、URL、登录等待时长）
- `logging`：全流程日志与异常记录
- `datetime`：到点判定与倒计时
- `time`：轮询节拍控制，到点前 5 秒切换 50ms 高频轮询

## 使用方法

```bash
# 指定浏览器与抢购时间
python shopingOnline.py -b edge -t "2026-08-11 21:00:00" --url https://www.jd.com

# 使用 chrome，登录等待 120 秒
python shopingOnline.py --browser chrome --login-wait 120
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `-b` / `--browser` | `edge` | 浏览器类型（edge/chrome/firefox） |
| `-t` / `--time` | 当前时间+60s | 抢购目标时间，格式 `YYYY-MM-DD HH:MM:SS` |
| `--url` | `https://www.jd.com` | 目标商城 URL |
| `--cart-url` | JD 购物车页 | 购物车 URL |
| `--login-wait` | `60` | 登录等待超时秒数 |

**流程说明：** 启动后自动打开商城首页并点击登录入口，请在浏览器中手动完成扫码/账密登录；脚本检测到登录态后自动打开购物车全选商品，等待到点后依次点击「去结算」「提交订单」。

## 目录结构

```
shopingOnline/
├── shopingOnline.py    # 主脚本
├── requirements.txt    # 依赖清单
├── LICENSE
└── README.md
```

## License

[MIT](LICENSE)

## 鸣谢（Acknowledgments）

感谢以下开源项目、工具与开发者（图标均取自官方站点 / CDN）：

<table>
  <tr>
    <td align="center" width="140">
      <a href="https://www.selenium.dev/">
        <img src="https://www.selenium.dev/images/selenium_logo_square_green.png" width="64" height="64" alt="Selenium" /><br />
        <sub><b>Selenium</b></sub>
      </a>
      <br />
      <sub>浏览器自动化</sub>
    </td>
    <td align="center" width="140">
      <a href="https://www.jetbrains.com/idea/">
        <img src="https://resources.jetbrains.com/storage/products/intellij-idea/img/meta/intellij-idea_logo_300x300.png" width="64" height="64" alt="IntelliJ IDEA" /><br />
        <sub><b>IntelliJ IDEA</b></sub>
      </a>
      <br />
      <sub>JetBrains 出品</sub>
    </td>
    <td align="center" width="140">
      <a href="https://www.jetbrains.com/pycharm/">
        <img src="https://resources.jetbrains.com/storage/products/pycharm/img/meta/pycharm_logo_300x300.png" width="64" height="64" alt="PyCharm" /><br />
        <sub><b>PyCharm</b></sub>
      </a>
      <br />
      <sub>JetBrains 出品</sub>
    </td>
  </tr>
</table>

| 项目 / 工具 | 贡献 | 许可证 |
|---|---|---|
| [Selenium](https://www.selenium.dev/) | 唯一的运行时依赖，承担全部浏览器自动化 | Apache-2.0 |
| [JetBrains](https://www.jetbrains.com/) | 提供 IntelliJ IDEA / PyCharm 等开发工具与开源支持 | 商业授权（开源项目可申请免费许可证） |
| Microsoft Edge / Google Chrome / Mozilla Firefox | 被驱动的目标浏览器与各自 WebDriver | 各浏览器自有许可证 |

> 参考来源：_（待补充，若本项目参考过其他抢购脚本，请在此署名）_
> 贡献者名单：_（待补充，欢迎在 PR 中署名）_

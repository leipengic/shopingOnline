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

## 鸣谢

- [Selenium](https://www.selenium.dev/)
- [JetBrains](https://www.jetbrains.com/) Open Source Support

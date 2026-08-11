"""JD 商城自动抢购脚本。

功能流程：登录 → 等待到点 → 结算 → 提交订单。
支持 edge/chrome/firefox 浏览器，命令行参数化配置。

用法示例::

    python shopingOnline.py -b edge -t "2026-08-11 21:00:00" --url https://www.jd.com
    python shopingOnline.py --browser chrome --login-wait 120
"""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys
import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_TARGET_URL = "https://www.jd.com"
DEFAULT_CART_URL = "https://cart.jd.com/cart_index"
DEFAULT_BROWSER = "edge"
DEFAULT_LOGIN_WAIT = 60
DEFAULT_TARGET_OFFSET_SECONDS = 60

# 页面元素定位常量
LOGIN_LINK_TEXT = "你好，请登录"
CHECKOUT_TEXT = "去结算"
CART_BODY_ID = "cart-body"
SUBMIT_ORDER_CLASS = "checkout-submit"


def setup_logging() -> None:
    """配置全局日志输出格式。"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="JD 商城自动抢购脚本：登录 → 等待到点 → 结算 → 提交订单",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-b", "--browser",
        choices=["edge", "chrome", "firefox"],
        default=DEFAULT_BROWSER,
        help="浏览器类型",
    )
    parser.add_argument(
        "-t", "--time",
        dest="time",
        default=None,
        help="抢购目标时间，格式 YYYY-MM-DD HH:MM:SS（默认当前时间+60秒）",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_TARGET_URL,
        help="目标商城 URL",
    )
    parser.add_argument(
        "--cart-url",
        dest="cart_url",
        default=DEFAULT_CART_URL,
        help="购物车 URL",
    )
    parser.add_argument(
        "--login-wait",
        dest="login_wait",
        type=int,
        default=DEFAULT_LOGIN_WAIT,
        help="登录等待超时秒数",
    )
    return parser.parse_args()


def parse_target_time(raw: Optional[str]) -> dt.datetime:
    """解析目标时间字符串。

    支持格式：
    - ``YYYY-MM-DD HH:MM:SS``
    - ``YYYY-MM-DD HH:MM:SS.ffffff``（带毫秒）

    当 ``raw`` 为 None 时，返回当前时间加上默认偏移秒数。

    Args:
        raw: 时间字符串或 None。

    Returns:
        解析后的 datetime 对象。

    Raises:
        ValueError: 时间字符串格式无法解析。
    """
    if not raw:
        target = dt.datetime.now() + dt.timedelta(seconds=DEFAULT_TARGET_OFFSET_SECONDS)
        logger.info(
            "未指定目标时间，默认使用当前时间 + %d 秒：%s",
            DEFAULT_TARGET_OFFSET_SECONDS,
            target.strftime("%Y-%m-%d %H:%M:%S"),
        )
        return target

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return dt.datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise ValueError(
        f"无法解析时间 '{raw}'，请使用格式 YYYY-MM-DD HH:MM:SS"
    )


def create_driver(browser_type: str) -> webdriver.Remote:
    """根据浏览器类型创建并返回 WebDriver 实例。

    Args:
        browser_type: 浏览器类型（edge/chrome/firefox）。

    Returns:
        已启动的 WebDriver 实例（调用方负责 quit）。

    Raises:
        ValueError: 不支持的浏览器类型。
        WebDriverException: 浏览器启动失败。
    """
    browser = browser_type.lower().strip()
    logger.info("正在创建 %s 浏览器实例...", browser)
    if browser == "edge":
        return webdriver.Edge()
    if browser == "chrome":
        return webdriver.Chrome()
    if browser == "firefox":
        return webdriver.Firefox()
    raise ValueError(
        f"不支持的浏览器类型：{browser_type}，请使用 edge/chrome/firefox"
    )


def safe_find_element(
    driver: webdriver.Remote,
    by: str,
    value: str,
    timeout: float = 10.0,
) -> Optional[WebElement]:
    """安全查找元素：等待元素可点击，超时返回 None。

    使用 WebDriverWait 显式等待，替代脆弱的 time.sleep 固定等待。
    所有 Selenium 支持的 by 字符串均可使用，如 ``"id"``、``"link text"``、
    ``"class name"``、``"css selector"``、``"xpath"`` 等。

    Args:
        driver: WebDriver 实例。
        by: 定位策略字符串（与 ``selenium.webdriver.common.by.By`` 常量值一致）。
        value: 定位值。
        timeout: 等待超时秒数。

    Returns:
        找到的 WebElement；超时未找到返回 None。
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    except TimeoutException:
        logger.warning("找不到元素 %s = %s", by, value)
        return None


def login(
    driver: webdriver.Remote,
    wait_timeout: int,
    target_url: str,
) -> None:
    """打开目标首页并触发登录流程，等待用户完成登录。

    登录完成判定：浏览器 URL 不再包含 ``passport`` 或 ``login``，
    表示已从登录页跳回主站。这种方式比固定 ``time.sleep`` 更可靠。

    Args:
        driver: WebDriver 实例。
        wait_timeout: 登录等待超时秒数。
        target_url: 目标商城 URL。
    """
    logger.info("打开目标首页：%s", target_url)
    driver.get(target_url)

    login_link = safe_find_element(driver, "link text", LOGIN_LINK_TEXT, timeout=15)
    if login_link is None:
        logger.warning("未找到登录入口（可能已登录），直接继续")
        return

    login_link.click()
    logger.info("已点击登录入口，请在浏览器中完成登录")

    # 等待跳转到登录页（最多 10 秒）
    try:
        WebDriverWait(driver, 10).until(
            lambda d: "passport" in d.current_url.lower()
            or "login" in d.current_url.lower()
        )
    except TimeoutException:
        logger.warning("未检测到登录页跳转，可能已处于登录态")

    # 等待登录完成（URL 离开登录页）
    try:
        WebDriverWait(driver, wait_timeout).until(
            lambda d: "passport" not in d.current_url.lower()
            and "login" not in d.current_url.lower()
        )
        logger.info("检测到登录完成")
    except TimeoutException:
        logger.warning("登录等待超时（%d 秒），继续后续流程", wait_timeout)


def prepare_cart(
    driver: webdriver.Remote,
    cart_url: str,
    wait_timeout: int,
) -> None:
    """打开购物车页面并选中所有商品。

    Args:
        driver: WebDriver 实例。
        cart_url: 购物车 URL。
        wait_timeout: 元素等待超时秒数。
    """
    logger.info("打开购物车页面：%s", cart_url)
    driver.get(cart_url)

    cart_body = safe_find_element(driver, "id", CART_BODY_ID, wait_timeout)
    if cart_body is not None:
        cart_body.click()
        logger.info("已选中购物车商品")
    else:
        logger.warning("未找到购物车主体元素 cart-body，继续后续流程")


def wait_for_target_time(target_time: dt.datetime) -> None:
    """等待至目标抢购时间。

    距离目标时间较远时低频轮询（每秒一次），最后 5 秒进入高频模式
    （每 50ms 一次）以提高抢购精度。

    注：此处为纯墙钟时间等待，WebDriverWait 设计用于等待页面元素条件，
    不适用于此场景，因此保留 ``time.sleep`` 进行轮询。所有页面元素
    等待均已改用 WebDriverWait 显式等待。

    Args:
        target_time: 目标抢购时间。
    """
    logger.info("等待至目标抢购时间：%s", target_time.strftime("%Y-%m-%d %H:%M:%S"))
    while dt.datetime.now() < target_time:
        remaining = (target_time - dt.datetime.now()).total_seconds()
        if remaining > 5:
            logger.info("距抢购开始还有 %.1f 秒", remaining)
            time.sleep(1.0)
        else:
            time.sleep(0.05)
    logger.info("到达目标抢购时间，开始执行抢购流程")


def checkout(driver: webdriver.Remote, wait_timeout: int) -> None:
    """点击“去结算”按钮进入结算流程。

    Args:
        driver: WebDriver 实例。
        wait_timeout: 元素等待超时秒数。

    Raises:
        RuntimeError: 超时未找到结算按钮。
    """
    logger.info("等待『去结算』按钮...")
    button = safe_find_element(driver, "link text", CHECKOUT_TEXT, wait_timeout)
    if button is None:
        raise RuntimeError("超时未找到『去结算』按钮")
    button.click()
    logger.info("已点击『去结算』")


def submit_order(driver: webdriver.Remote, wait_timeout: int) -> None:
    """点击“提交订单”按钮完成下单。

    Args:
        driver: WebDriver 实例。
        wait_timeout: 元素等待超时秒数。

    Raises:
        RuntimeError: 超时未找到提交订单按钮。
    """
    logger.info("等待『提交订单』按钮...")
    button = safe_find_element(driver, "class name", SUBMIT_ORDER_CLASS, wait_timeout)
    if button is None:
        raise RuntimeError("超时未找到『提交订单』按钮")
    button.click()
    logger.info("抢购成功，请尽快付款")


def main() -> None:
    """脚本主入口。

    流程：解析参数 → 创建浏览器 → 登录 → 准备购物车 → 等待到点 → 结算 → 提交订单。
    任何异常都会被捕获并记录；finally 中等待用户按回车后再关闭浏览器，
    以便用户在抢购完成后进行付款操作。
    """
    args = parse_args()
    setup_logging()

    try:
        target_time = parse_target_time(args.time)
    except ValueError as e:
        print(f"参数错误：{e}", file=sys.stderr)
        sys.exit(2)

    if target_time <= dt.datetime.now():
        logger.warning(
            "目标时间 %s 已过期，将立即开始抢购流程",
            target_time.strftime("%Y-%m-%d %H:%M:%S"),
        )

    logger.info("=== JD 抢购脚本启动 ===")
    logger.info("浏览器类型：%s", args.browser)
    logger.info("目标 URL：%s", args.url)
    logger.info("购物车 URL：%s", args.cart_url)
    logger.info("目标抢购时间：%s", target_time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("登录等待超时：%d 秒", args.login_wait)

    driver: Optional[webdriver.Remote] = None
    try:
        driver = create_driver(args.browser)
        login(driver, args.login_wait, args.url)
        prepare_cart(driver, args.cart_url, args.login_wait)
        wait_for_target_time(target_time)
        checkout(driver, args.login_wait)
        submit_order(driver, args.login_wait)
        logger.info("=== 抢购流程执行完毕 ===")
    except KeyboardInterrupt:
        logger.info("用户中断操作")
    except Exception as e:
        logger.exception("抢购流程异常：%s", e)
    finally:
        if driver is not None:
            try:
                input("按回车关闭浏览器...")
            except (EOFError, KeyboardInterrupt):
                pass
            try:
                driver.quit()
                logger.info("浏览器已关闭")
            except Exception as e:
                logger.warning("关闭浏览器时出错：%s", e)


if __name__ == "__main__":
    main()

import datetime
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# 优化1：将配置信息外部化，提高代码的灵活性
browser_type = "edge"
target_url = "https://www.jd.com"
cart_url = "https://cart.jd.com/cart_index"
checkout_text = "去结算"
submit_order_text = "提交订单"

# 优化2：使用更精细的异常处理
def safe_find_element(by, value):
    try:
        return WebBrowser.find_element(by, value)
    except NoSuchElementException:
        print(f"找不到 {by} = {value} 的元素")
        return None

# 优化3：使用with语句管理资源
with webdriver.Edge() as WebBrowser:
    WebBrowser.get(target_url)
    time.sleep(3)

    # 登录操作（示例，需根据实际情况调整）
    WebBrowser.find_element("link text","你好，请登录").click()
    time.sleep(10)

    WebBrowser.get(cart_url)
    time.sleep(3)

    # 优化4：减少嵌套的无限循环，简化逻辑
    while True:
        cart_body_element = safe_find_element("id", "cart-body")
        if cart_body_element:
            cart_body_element.click()
            break

    # 实时时间比较优化
    now = datetime.datetime.now()
    mstime = datetime.datetime.strptime("2023-03-24 21:00:00.000000", '%Y-%m-%d %H:%M:%S.%f')

    while now < mstime:
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d %H:%M:%S.%f'))

    # 结算操作
    while True:
        checkout_button = safe_find_element("link text", checkout_text)
        if checkout_button:
            checkout_button.click()
            print(f"结算成功")
            break

    # 提交订单操作
    while True:
        submit_order_button = safe_find_element("class name", "checkout-submit")
        if submit_order_button:
            submit_order_button.click()
            print(f"抢购成功，请尽快付款")
            break

    # 优化5：不再需要无限循环来保持程序运行
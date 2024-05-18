import datetime
import time
from selenium import webdriver

# 加载所需的库

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
mstime = "2023-03-24 21:00:00.000000"
# 首先我们需要设置抢购的时间，格式要按照预设的格式改就可以了，个月数的一定在前面加上0，例如 “01”

WebBrowser = webdriver.Edge()
# 选择使用的浏览器，如果没有Chrome浏览器可以更改其他浏览器

# 淘宝 WebBrowser.get("https://www.taobao.com")
WebBrowser.get("https://www.jd.com")
time.sleep(3)
# 获取网站

# WebBrowser.find_element("link text", "亲，请登录").click()
WebBrowser.find_element("link text","你好，请登录").click()
print(f"请扫码登录")
time.sleep(10)
# 进入网站后读取登录链接，并扫码登录

# 淘宝 WebBrowser.get("https://cart.taobao.com/cart.htm")
WebBrowser.get("https://cart.jd.com/cart_index")
time.sleep(3)
# 登录后直接转跳到购物车页面

while True:
    try:
        #   if WebBrowser.find_element("id", "J_SelectAll1"):
        #   WebBrowser.find_element("id", "J_SelectAll1").click()
        if WebBrowser.find_element("id", "cart-body"):
            WebBrowser.find_element("id", "cart-body").click()
            break
            # 这里代码意思是找到购物车全选的按钮并点击全选
    except:
        print(f"找不到购买按钮")
while True:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(now)
    # print(now) 可以将实时的时间输出出来
    if now > mstime:
        # 当当前时间超过了抢购时间就立刻执行下面代码
        while True:
            try:
                #if WebBrowser.find_element("link text", "结 算"):
                    # WebBrowser.find_element("link text", "结 算").click()
                if WebBrowser.find_element("link text", "去结算"):
                    WebBrowser.find_element("link text", "去结算").click()
                    print(f"结算成功")
                    break
                    # 识别界面中的“结算”按钮并点击
            except:
                pass
        while True:
            try:
                #if WebBrowser.find_element("link text", '提交订单'):
                    #WebBrowser.find_element("link text", '提交订单').click()
                if WebBrowser.find_element("class name", "checkout-submit"):
                    WebBrowser.find_element("class name", "checkout-submit").click()
                    print(f"抢购成功，请尽快付款")
                    # 和上面同理，识别界面中的“提交订单”按钮
            except:
                print(f"结算提交成功,已抢到商品啦,请及时支付订单")
                break
        time.sleep(0.01)
# 手动登录后，保存cookies
import os#与操作系统进行交互
import pickle#用于保存和加载 Cookies
from selenium import webdriver#用于自动化浏览器操作，模拟用户登录过程
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time#用于添加时间延迟，确保页面元素加载完成

def login_bilibili():
    driver_path = 'D:/Downroads/edgedriver_win64/msedgedriver.exe'#Edge浏览器v136
    service = Service(driver_path)#创建一个 Service 对象，用于启动 Edge 浏览器驱动
    driver = webdriver.Edge(service=service)#创建一个 Edge 浏览器实例
    
    driver.get('https://www.bilibili.com')
    cookies_file = 'bilibili_cookies.pkl'#定保存 Cookies 的文件名

    # 如果有cookies文件，直接加载
    if os.path.exists(cookies_file):
        print("🔵 检测到本地Cookies，正在加载...")
        with open(cookies_file, 'rb') as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5)

        try:
            # 等待登录成功用户头像元素加载完成
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bili-avatar'))
            )
            print("✅ 成功通过Cookies登录！")
            return driver
        except:
            print("⚠️ Cookies失效，准备手动登录...")
    else:
        # 如果没有cookies或cookies失效，则手动登录
        print("🟡 请手动登录...")
        driver.get('https://passport.bilibili.com/login')
        
        # 输入用户名和密码，这里需要替换为你的真实信息
        username = '******'
        password = '******'

        # 等待账号输入框加载完成
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="账号"]/following-sibling::input'))
        )

        # 找到密码输入框并输入信息
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[text()="密码"]/following-sibling::input'))
        )
        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.btn_primary'))
        )
        # 点击登录按钮
        login_button.click()

        time.sleep(80)  # 给你时间手动扫码/输入账号，处理验证码

        # 登录完成后保存cookies
        cookies = driver.get_cookies()
        with open(cookies_file, 'wb') as f:
            pickle.dump(cookies, f)
        print("✅ 登录完成，Cookies已保存！")
        
    return driver
from selenium import webdriver
from selenium.webdriver.common.by import By#用于定位元素
from selenium.webdriver.support.ui import WebDriverWait#用于等待元素加载
from selenium.webdriver.support import expected_conditions as EC#用于设置等待条件
from selenium.webdriver.common.keys import Keys#用于模拟键盘操作
import time

def search_videos(driver, keyword):
    # 打开B站主页
    driver.get("https://www.bilibili.com")

    # 等待搜索框加载
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "nav-searchform"))
    )

    # 构造搜索 URL
    search_url = f"https://search.bilibili.com/all?keyword={keyword}"
    driver.get(search_url)

    # 等待搜索结果加载
    time.sleep(6)# 等待页面加载完成
    print("🔵 搜索结果加载完成，正在获取视频链接...")

    # 等待视频卡片加载
    WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bili-video-card"))
        )
    # 获取前3个视频链接
    cards = driver.find_elements(By.CLASS_NAME, "bili-video-card")[:3]
    
    video_links = []
    for card in cards:  # 获取cards视频链接
        try:
            # 定位元素标签提取链接、标题
            link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            title = card.find_element(By.TAG_NAME, 'h3').get_attribute('title')
            print(f"视频标题: {title}\n视频链接: {link}\n")
            if link:
                video_links.append(link)#添加到 video_links 列表中
        except Exception as e:
            print("解析失败：", e)
    
    return video_links

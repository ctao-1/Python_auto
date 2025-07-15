from selenium.webdriver.common.by import By#用于定位元素
from selenium.webdriver.support.ui import WebDriverWait#用于等待元素加载完成
from selenium.webdriver.support import expected_conditions as EC#用于设置等待条件
import time

def get_hot_videos(driver, video_links):
    video_data = []

    for link in video_links:
        driver.get(link)
        time.sleep(3)

        try:
            title_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.video-title.special-text-indent'))
            )
            title = title_elem.text
        except:
            title = "标题获取失败"

        try:
            play_elem = driver.find_element(By.CLASS_NAME, 'view-text')
            plays = play_elem.text
        except:
            plays = "播放量获取失败"

        try:
            like_elem = driver.find_element(By.CSS_SELECTOR, '.video-like-info.video-toolbar-item-text')
            likes = like_elem.text
        except:
            likes = "点赞数获取失败"

        try:
            comment_elem = driver.find_element(By.CLASS_NAME, 'dm')
            comments = comment_elem.text
        except:
            comments = "弹幕数获取失败"

        video_data.append({
            'url': link,
            'title': title,
            'plays': plays,
            'likes': likes,
            'comments': comments
        })

        print(f"\n标题: {title}\n播放量: {plays}\n点赞: {likes}\n弹幕: {comments}\n链接: {link}")

    return video_data

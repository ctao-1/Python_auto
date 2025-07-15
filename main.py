from bilibili_auto_login import login_bilibili
from search import search_videos
from video_crawler import get_hot_videos#爬视频基本信息
from comments_crawler import get_comments#抓取评论
from sentiment_analysis import analyze_sentiment, plot_sentiment_distribution
from generate_comment import generate_ai_comment
import time

def main():
    driver = login_bilibili()

    keyword = input("请输入要搜索的视频关键词：")
    video_links = search_videos(driver, keyword)

    print("\n正在获取热门视频信息...")
    hot_video_data = get_hot_videos(driver, video_links)

    j = 0
    for video in hot_video_data:
        j += 1
        print(f"\n处理视频{j}：{video['title']}")
        comments = get_comments(video['url'])

        print("📊 正在分析评论情感...")
        sentiment_result = analyze_sentiment(comments)
        plot_sentiment_distribution(sentiment_result)

        ai_comment = generate_ai_comment(comments)
        print("AI自动生成评论：", ai_comment)

    time.sleep(10)
    driver.quit()

if __name__ == '__main__':
    main()

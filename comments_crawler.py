import requests#发送 HTTP 请求，获取网页内容或 API 响应
from bs4 import BeautifulSoup#解析 HTML 文档
import re#正则表达式模块，用于字符串匹配和提取

def bv2av(bv_id):
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bilibili.com"
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"请求失败，状态码: {res.status_code}")
            return None

        if not res.text.strip().startswith("{"):
            print("返回内容非JSON格式，可能被拦截或出错")
            print(res.text[:200])  # 打印前200字符帮助调试
            return None

        res_json = res.json()
        if res_json["code"] == 0:
            return res_json["data"]["aid"]
        else:
            print("BV号转换失败，返回code非0")
            return None
    except Exception as e:
        print("请求 BV 转 AV 接口出错：", e)
        return None

def extract_comment_from_html(html):
    """
    提取HTML中的评论内容，处理多个 <p id="contents"> 元素，解析表情和文本
    """
    soup = BeautifulSoup(html, 'html.parser')
    p_list = soup.find_all("p", id="contents")
    full_text = ""
    for p in p_list:
        for element in p.contents:
            if element.name == "img":
                full_text += element.get("alt", "")
            elif element.name == "span":
                full_text += element.get_text()
            elif isinstance(element, str):
                full_text += element.strip()#拼接完整文本
    return full_text.strip()


def get_comments(video_url):
    match = re.search(r'/video/(BV\w+)', video_url)
    if not match:
        print("未能提取视频BV号")
        return []

    bv_id = match.group(1)
    aid = bv2av(bv_id)
    if not aid:
        return []

    api_url = f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid}&sort=2&pn=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': video_url
    }

    try:
        res = requests.get(api_url, headers=headers).json()
        comment_list = []
        if res["code"] == 0:
            replies = res["data"].get("replies", [])
            i = 0
            for item in replies[:3]:  # 热门前三条评论
                content = item.get("content", {})
                if "rich_text" in content and content["rich_text"]:
                    html = content["rich_text"]
                    comment = extract_comment_from_html(html)#带 HTML 标签的评论（包含表情、样式）
                else:
                    comment = content.get("message", "")#普通纯文本评论
                if comment:
                    comment_list.append(comment)
                    i += 1
                    print(f"热门评论{i}: {comment}")                    
        else:
            print("评论接口请求失败")
            return []
    except Exception as e:
        print("请求评论接口异常：", e)
        return []

    print(f"抓取到 {len(comment_list)} 条热门评论")
    return comment_list


if __name__ == "__main__":
    url = "https://www.bilibili.com/video/BV1Xx411c7mD"
    comments = get_comments(url)
    for i, c in enumerate(comments, 1):
        print(f"热门评论{i}: {c}")
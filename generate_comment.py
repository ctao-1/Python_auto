import requests

# 硅基流动 API 设置
GLM_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
GLM_API_KEY = "sk-dutoqtmqkqobfctlzfzvfpzdhdtdieyjcfmxlwjnbdseowai"  # 🔁 自己的密钥

def generate_ai_comment(comments):
    """
    使用硅基流动的大模型生成AI自动评论。
    参数:
        comments (list): 字符串形式的评论列表。
    返回:
        str: AI生成的评论文本。
    """
    if not comments:
        return "评论区还没有声音呢，欢迎你来留下第一条留言~"

    prompt = (
        "以下是一些B站视频下的用户评论，请你总结评论区的整体情绪，"
        "并以第一人称的口吻生成一句有共鸣、自然、温暖的自动评论：\n"
        + "\n".join(comments[:10])
    )

    payload = {
        "model": "Qwen/QwQ-32B",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "max_tokens": 100,
        "enable_thinking": False,
        "thinking_budget": 512,
        "min_p": 0.05,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
        "tools": []  # 可省略，如果不使用函数调用
    }

    headers = {
        "Authorization": f"Bearer {GLM_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GLM_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        # 提取回答内容
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("❌ AI评论生成失败：", e)
        return "AI评论生成失败！"

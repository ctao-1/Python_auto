from snownlp import SnowNLP# 导入 SnowNLP 库
import matplotlib.pyplot as plt# 导入 Matplotlib 库

# 设置中文字体为 SimHei，如果你在 Windows 中使用
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义情感分析函数
def analyze_sentiment(comments):
    sentiment_result = {'positive': 0, 'neutral': 0, 'negative': 0}
    for comment in comments:
        s = SnowNLP(comment)
        score = s.sentiments  # 得分范围 0~1
        if score > 0.6:
            sentiment_result['positive'] += 1
        elif score < 0.4:
            sentiment_result['negative'] += 1
        else:
            sentiment_result['neutral'] += 1
    return sentiment_result

#定义绘制情感分布柱状图的函数
def plot_sentiment_distribution(result):
    labels = ['积极', '中性', '消极']
    counts = [result['positive'], result['neutral'], result['negative']]
    colors = ['#4caf50', '#ffc107', '#f44336']

    plt.figure(figsize=(6, 4))
    plt.bar(labels, counts, color=colors)
    plt.title('评论情感分布')
    plt.xlabel('情感类型')
    plt.ylabel('评论数量')
    plt.tight_layout()
    plt.savefig('sentiment_distribution.png')
    plt.show()

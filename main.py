import os
import requests
from google import genai

# 1. 读取环境变量
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
APP_TOKEN = os.environ.get("WXPUSHER_APP_TOKEN")
USER_UID = os.environ.get("WXPUSHER_UID")

# 2. 初始化 Gemini 客户端
client = genai.Client(api_key=GEMINI_API_KEY)

def get_daily_stock_news():
    prompt = """
    请整理今天美股最新的50条英文要闻与市场动态。
    格式要求：
    1. 使用 HTML 格式输出（不要 markdown 代码块，直接返回 <h3> 和 <ul>/<li> 标签）。
    2. 按分类整理（如 Macro & Geopolitics, Tech & AI, Energy, Healthcare 等）。
    3. 每条新闻保留英文原文，并附带简短中文翻译与点评。
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def send_to_wxpusher(content):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": APP_TOKEN,
        "content": content,
        "contentType": 2,  # 2 代表 HTML 格式
        "summary": "今日美股50条最新动态",
        "uids": [USER_UID]
    }
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url, json=payload)
    print("推送结果：", res.json())

if __name__ == "__main__":
    news_html = get_daily_stock_news()
    send_to_wxpusher(news_html)

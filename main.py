import os
import requests
import google.generativeai as genai

# 1. 初始化配置
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
APP_TOKEN = os.environ.get("WXPUSHER_APP_TOKEN")
USER_UID = os.environ.get("WXPUSHER_UID")

# 2. 调用 Gemini 生成新闻
def get_daily_stock_news():
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    请整理今天美股最新的50条英文要闻与市场动态。
    格式要求：
    1. 使用 HTML 格式输出（不要 markdown 代码块，直接返回 <h3> 和 <ul>/<li> 标签）。
    2. 按分类整理（如 Macro, Tech, Energy 等）。
    3. 每条新闻保留英文原文，并附带简短中文翻译与点评。
    """
    
    response = model.generate_content(prompt)
    return response.text

# 3. 发送到 WxPusher
def send_to_wxpusher(content):
    url = "http://wxpusher.zhengxianbao.com/api/send/message"
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

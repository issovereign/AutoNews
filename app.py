from flask import Flask, request, render_template_string, jsonify
from generate_fake_news import generate_fake_news
import threading
import time
import os
import uuid

app = Flask(__name__)

# 簡單的任務暫存（正式環境建議用 Redis、資料庫等）
task_results = {}

@app.route('/')
def home():
    return '''
        <html>
            <head>
                <title>Fake News Generator</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    input[type=text] { padding: 10px; width: 300px; margin-right: 10px; }
                    input[type=submit] { padding: 10px 20px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
                    input[type=submit]:hover { background-color: #0056b3; }
                </style>
            </head>
            <body>
                <h2>請輸入欲查詢之科技新聞關鍵字與OpenAI api key，本網站將生成相關假新聞</h2>
                <form action="/news" method="post">
                    <input name="keyword" type="text" placeholder="輸入科技新聞關鍵字"/>
                    <input name="api_key" type="text" placeholder="輸入OpenAI api key"/>
                    <input type="submit" value="開始生成"/>
                </form>
            </body>
        </html>
    '''

@app.route('/news', methods=['POST'])
def upload_news():
    print("✅ POST /news 被呼叫了")
    keyword = request.form['keyword']
    api_key = request.form['api_key']
    task_id = str(uuid.uuid4())
    task_results[task_id] = {"status": "pending"}

    # 背景執行 GPT 任務
    threading.Thread(target=run_task, args=(task_id, api_key, keyword)).start()

    return render_template_string('''
        <html>
            <head>
                <title>生成中...</title>
                <script>
                    async function checkStatus() {
                        const response = await fetch('/result/{{ task_id }}');
                        const data = await response.json();
                        if (data.status === 'done') {
                            window.location.href = "/result_view/{{ task_id }}";
                        } else {
                            setTimeout(checkStatus, 2000);
                        }
                    }
                    window.onload = checkStatus;
                </script>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
                    .loading { font-size: 24px; color: #555; margin-top: 100px; }
                </style>
            </head>
            <body>
                <div class="loading">AI 正在生成假新聞中，請稍候...</div>
            </body>
        </html>
    ''', task_id=task_id)

def run_task(task_id, api_key, keyword):
    try:
        fake_news = generate_fake_news(api_key, keyword=keyword)
        title, content = fake_news.split('\n', 1)
        task_results[task_id] = {
            "status": "done",
            "title": title[3:].strip(),
            "content": content[3:].strip()
        }
    except Exception as e:
        task_results[task_id] = {
            "status": "error",
            "message": str(e)
        }

@app.route('/result/<task_id>')
def check_result(task_id):
    result = task_results.get(task_id)
    if not result:
        return jsonify({"status": "not_found"})
    return jsonify(result)

@app.route('/result_view/<task_id>')
def result_view(task_id):
    result = task_results.get(task_id)
    if not result or result["status"] != "done":
        return "尚未完成或發生錯誤", 400

    title = result["title"]
    content = result["content"]

    return render_template_string('''
        <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                        color: #333;
                    }
                    .container {
                        max-width: 800px;
                        margin: auto;
                        padding: 20px;
                        background-color: #fff;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    h1, p {
                        margin-bottom: 20px;
                    }
                    p {
                        line-height: 1.6;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ title }}</h1>
                    <p>{{ content }}</p>
                </div>
            </body>
        </html>
    ''', title=title, content=content)

if __name__ == '__main__':
    app.run(debug=True)
    # port = int(os.environ.get("PORT", 5000))  # Render 預設傳入 PORT 環境變數
    # app.run(host='0.0.0.0', port=port, debug=False)

    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)

from flask import Flask, request, render_template_string
from generate_fake_news import generate_fake_news
import os

app = Flask(__name__)

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
    keyword = request.form['keyword']
    api_key = request.form['api_key']
    fake_news = generate_fake_news(api_key, keyword=keyword)
    title, content = fake_news.split('\n', 1)
    title = title[3:]
    content = content[3:]

    return render_template_string('''
        <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;  /* 背景颜色 */
                        color: #333;  /* 文本颜色 */
                    }
                    .container {
                        max-width: 800px;
                        margin: auto;  /* 上下保持不变，左右自动留白 */
                        padding: 20px;
                        background-color: #fff;  /* 容器背景颜色 */
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);  /* 添加一些阴影效果 */
                    }
                    h1, p {
                        margin-bottom: 20px;  /* 添加一些底部外边距 */
                    }
                    p {
                        line-height: 1.6;  /* 增加行高 */
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
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))  # Render 預設傳入 PORT 環境變數
    app.run(host='0.0.0.0', port=port, debug=True)

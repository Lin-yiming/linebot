# -*- coding: utf-8 -*-
"""
創建於 2021年6月2日 21:16:35

作者：Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡 ivanyang0606@gmail.com

Line Bot 聊天機器人
第三章 互動回傳功能
傳送貼圖 StickerSendMessage
"""
# 載入所需的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import json

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('sLqfuHAML8w7edfahcrCXiqhvh8DKPm29T6DXobKZAAsFnc9KX4OsdxIImyMlTUPGmq4uZ+73nWnGa0vfIRRM+TgxK53OIkI+I0Bt7E4CaCuBy8oYwtzKvUet56jW5oF/6H7jCgEWFoJZAatfEp/OAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的 Channel Secret
handler = WebhookHandler('ac1c39cba994874c70d504130e80e92e')

line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 X-Line-Signature 標頭值
    signature = request.headers['X-Line-Signature']

    # 將請求內容作為文本獲取
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 檢查是否為確認通信請求
    try:
        json_data = json.loads(body)
        if 'events' in json_data and not json_data['events']:
            return 'OK', 200
    except json.JSONDecodeError:
        pass

    # 處理 webhook 請求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

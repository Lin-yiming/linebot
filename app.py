# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第三章 互動回傳功能
推播push_message與回覆reply_message
"""
# 載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import json

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('6Mux3gHBehpFUIg8DruP0+DpoXKQ2Lzwz0jt+OavFtBtn4Py63dI96z0IIKP3KTV/uLu+2sKGEyruYYnn/aG5zYv6aiLkTWQ3KIJ96ypEG/dwnj2Yrdw9mt+3aImofyITcdZtD/QPI0lhhjpcZlxQQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('3237ed691fa046813aedd176f227e36b')

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

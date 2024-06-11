# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第三章 互動回傳功能
傳送貼圖StickerSendMessage
"""
# 載入LineBot所需要的套件
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import pytz
import json
import os

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('M0VcXEA3fVeiGv9nyqwVLRYPKD8GNwSUIiKvkZ110SOd0kxUtuu8lJOjNEb/KQcDnuX0HPz1qoNh9+Gliu0zFLUDsVFXKdaVZjSGnFncYr1e88wAB3HuFzp1L+Rk0jgLf+2DlxxWtsAjzuaREDLzBwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('82780a5fa0d3cd286da66afc02a8f6d8')

line_bot_api.push_message('U2d2c861cb54857d9f7faf78587d3af62', TextSendMessage(text='你可以開始了'))

# 設定台北時區
taipei_tz = pytz.timezone('Asia/Taipei')

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

# 定義增加提醒功能
def add_reminder(user_id, remind_datetime, message):
    # 動態創建定時任務
    scheduler.add_job(
        func=send_reminder,
        trigger=DateTrigger(run_date=remind_datetime),
        args=[user_id, message],
        id=f"{user_id}_{remind_datetime.strftime('%Y%m%d%H%M%S')}",
        replace_existing=True
    )

# 定義發送提醒功能
def send_reminder(user_id, message):
    line_bot_api.push_message(user_id, TextSendMessage(text=message))

# 增加特定日期的提醒通知
def add_specific_date_reminders():
    user_id = 'U2d2c861cb54857d9f7faf78587d3af62'
    remind_dates = [
        "2024-06-02", "2024-06-05", "2024-06-08", "2024-06-10",
        "2024-06-14", "2024-06-15", "2024-06-16", "2024-06-17",
        "2024-06-20", "2024-06-22", "2024-06-24", "2024-06-25",
        "2024-06-26", "2024-06-27", "2024-06-29", "2024-06-30"
    ]
    for date_str in remind_dates:
        remind_datetime = taipei_tz.localize(datetime.strptime(date_str + " 09:00", '%Y-%m-%d %H:%M'))
        message = f"提醒你今天要上班！{date_str}"
        add_reminder(user_id, remind_datetime, message)

# 主程式
if __name__ == "__main__":
    # 啟動排程器
    scheduler = BackgroundScheduler()
    scheduler.start()

    # 增加特定日期的提醒
    add_specific_date_reminders()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

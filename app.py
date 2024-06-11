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
import re
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
import pytz

app = Flask(__name__)

# 必須放上自己的 Channel Access Token
line_bot_api = LineBotApi('sLqfuHAML8w7edfahcrCXiqhvh8DKPm29T6DXobKZAAsFnc9KX4OsdxIImyMlTUPGmq4uZ+73nWnGa0vfIRRM+TgxK53OIkI+I0Bt7E4CaCuBy8oYwtzKvUet56jW5oF/6H7jCgEWFoJZAatfEp/OAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的 Channel Secret
handler = WebhookHandler('ac1c39cba994874c70d504130e80e92e')

line_bot_api.push_message('Uae4d95a8996273cbd5fd013544cb3d5a', TextSendMessage(text='你可以開始了'))

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

    # 如果 body 中的 events 為空，返回 200 狀態碼
    if body and 'events' in body and len(eval(body)['events']) == 0:
        return 'OK', 200

    # 處理 webhook 請求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 訊息傳遞區塊
##### 基本上程式編輯都在這個 function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if re.match('告訴我秘密', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('才不告訴你哩！'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

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
    user_id = 'Uae4d95a8996273cbd5fd013544cb3d5a'
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

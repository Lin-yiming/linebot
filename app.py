import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageMessage
from linebot.exceptions import LineBotApiError
import requests

# 初始化 Line Bot API
line_bot_api = LineBotApi('p7Cmx4BoCNt0LD2kgdfeOe75gPTHF3sLGrR099KNnnrTdJK5RBzaAxB58kQs7XWmOlKesfndO2M6Nl9q4SeYn7+700i3CqocUHqzN+TeBZoCiktCjDL5w9fLfW9ed++jljaF0zYUhp620TxhWDkeTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('980186763ec26279c6c95254f44a4ae8')

# 接收 Line Bot 的訊息事件
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    image = message_content.content
    # 將圖片上傳到 Imgur
    imgur_url = upload_to_imgur(image)
    reply_message = f"Your image is uploaded to {imgur_url}"
    line_bot_api.reply_message(event.reply_token, TextMessage(text=reply_message))

def upload_to_imgur(image):
    client_id = 'd6f8a94c37e2b83'
    headers = {'Authorization': f'Client-ID {client_id}'}
    url = 'https://api.imgur.com/3/image'
    files = {'image': image}
    response = requests.post(url, headers=headers, files=files)
    data = response.json()
    imgur_url = data['data']['link']
    return imgur_url

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

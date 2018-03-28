from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)

line_bot_api = LineBotApi('7GVe4vSGcvJHq9bOy7BOnBU7Z1XVIyn1W9DwGm8tiRAnHR7TfAeZW6dxosASoGfDs7qnvNiBWnhnpv2bBQ1DwIsAAsGaHN2yyay/LGoWEe1hAuvYk6+8dU8q+sSxnIdwHTxH3BgZLua8nn9EKw0KwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2b2878273b5deece42488219dc3f1617')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
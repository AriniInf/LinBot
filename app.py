from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests
import re
import requests, json

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('T+0+0kzZgup0S3wDUz7hEBPTXOyy+F6yXmuZfWFPlrmFW90hPOEa6ZOzKsQMpLU9A5FJp+nymQ241b4owCYkcBoDihA/uEp7n5SYrVZ0wJrA3m7C63IM+CZo3WaWxI76NfXGPcog+77ZICXZL8HXiwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c74db2f3b611a0c6f4651d231dc71fdb')
#===========[ NOTE SAVER ]=======================
notes = {}

#REQUEST NAMA SURAT
def carisurat(nomorsurat):
    URLsurat = "https://api.banghasan.com/quran/format/json/surat"+nomorsurat+"/"+"pre"
    r = requests.get(URLsurat)
    data = r.json()
    err = "data tidak ditemukan"

    status = data['status']
    if(status == "ok"):
        nomor_surat = data['hasil'][0]['nomor']
        nama_surat = data['hasil'][0]['nama']
        asma = data['hasil'][0]['asma']
        ayat = data['hasil'][0]['ayat']
        arti = data['hasil'][0]['arti']
        ket = data['hasil'][0]['keterangan']

        data = "Surat ke : "+nomor_surat+"\nNama Surat : "+nama_surat+"\nAsma Surat : "+asma+"\nJumlah Ayat : "+ayat+"\nKeterangan : "+keterangan
        return (data)

    elif(status == "error"):
        return (err)

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receive message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

    data=text.split('-')
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carisurat(data[1])))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

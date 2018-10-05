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
line_bot_api = LineBotApi('nCheFomZPKA81EfMCsgkGDaLIWlGlRdX/i9N4JAa2Vvetw4iB0iKyhX9EushTlct8Xm14AjoAhxifXP1THdjBLoIxT6bruyTKY10+M2Ea5iX0p9zraG/0kFvirKsv4vFV7SyYR7IAuEJvSyzvQDwMAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('a13be1528f294201578d36297fc549a6')
#===========[ NOTE SAVER ]=======================
notes = {}

#REQUEST DATA MHS
def carimhs(input):
    URLmhs = "https://www.pricelist.padmapratama.com/api/mhs.php?nrp=" + input
    irham = requests.get(URLmhs)
    data = irham.json()
    err = "data tidak ditemukan"
    
    flag = data['kode']
    if(flag == "1"):
        nrp = data['data_angkatan'][0]['nrp']
        nama = data['data_angkatan'][0]['nama']
        kos = data['data_angkatan'][0]['kosan']

        return nama + '\n' + nrp + '\n' + kos
    elif(flag == "0"):
        return err    

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
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=carimhs(text)))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="masuk"))
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

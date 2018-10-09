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
line_bot_api = LineBotApi('bsm50AlkCUYtBXN1LAmT3lFY14/aLI+O5n/kQQrmiTqJ5ukj43qhzGiamcd8ar83I15ZYIlEGKq9HxdJ7OUtfzzH4QXTkmbnLQRO+4s/xfNOLVOAGmLDWzCl1p43p633t5BaIybGVA+d+Qbd/cPeGwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('aad04b7b25a615c260c3c0b6a3f8352d')
#===========[ NOTE SAVER ]=======================
notes = {}

#REQUEST DATA MHS
def carimhs(nrp):
    URLmhs = "http://www.aditmasih.tk/api_ariniinf/view.php?nrp=" + nrp
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nrp = data['data_angkatan'][0]['NRP']
        nama = data['data_angkatan'][0]['Nama']
        kos = data['data_angkatan'][0]['Alamat']

        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "Nama : "+nama+"\nNrp : "+nrp+"\nKosan : "+kos
        return data
        # return all_data

    elif(flag == "0"):
        return err 
#INPUT DATA MHS
def inputmhs(nama, nrp, kosan):
    r = requests.post("http://www.aditmasih.tk/api_ariniinf/insert.php", data={'Nama': nama, 'NRP': nrp, 'Alamat': kosan})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nama+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'
#DELETE DATA MHS
def hapusmhs(nrp):
    r = requests.post("http://www.aditmasih.tk/api_ariniinf/delete.php", data={'Nrp': nrp})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+nrp+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

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
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=carimhs(text)))
    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="masuk"))
    data=text.split('-')
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='insert'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2],data[3])))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

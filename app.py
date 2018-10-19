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
    
    if 'error' not in data:

        nomor = data['hasil'][0]['nomor']
        nama = data['hasil'][0]['nama']
        asma = data['hasil'][0]['asma']
        name = data['hasil'][0]['name']
        start = data['hasil'][0]['start']
        ayat = data['hasil'][0]['ayat']
        tipe = data['hasil'][0]['type']
        urut = data['hasil'][0]['urut']
        rukuk = data['hasil'][0]['rukuk']
        arti = data['hasil'][0]['arti']
        keterangan = data['hasil'][0]['keterangan']

        data= "Nama_Surat : "+nama+"\nsuratke- : "+nomor+"\nArti : "+arti+"Jumlah_Ayat : "+ayat+"\nDiturunkan_di : "+tipe+"\nKeterangan : "+keterangan
        return data
 
    if 'error' in data:
        err = data['error']
        print(err)

def cariayatrandom()
    URLacak = "https://api.banghasan.com/quran/format/json/acak/pre"       
        r = requests.get(URLacak)
        data = r.json()
    
    if 'error' not in data:


        bhs= data['acak']['id']['id']
        surat= data['acak']['id']['surat']
        ayt= data['acak']['id']['ayat']
        teks= data['acak']['id']['teks']
        
        bahasa= data['acak']['ar']['id']
        srt= data['acak']['ar']['surat']
        ayatar= data['acak']['ar']['ayat']
        texar= data['acak']['ar']['teks']

        nomor = data['surat']['nomor']
        nama = data['surat']['nama']
        asma = data['surat']['asma']
        name = data['surat']['name']
        start = data['surat']['start']
        ayat = data['surat']['ayat']
        tipe = data['surat']['type']
        urut = data['surat']['urut']
        rukuk = data['surat']['rukuk']
        arti = data['surat']['arti']
        keterangan = data['surat']['keterangan']

        data= "Nama_Surat : "+nama+"\nsuratke- : "+surat+"\nAyat : "+ayt+"\nteks : "+texar+"\nArti : "+ teks
        return data
 
    if 'error' in data:
        err = data['error']
        print(err)

def cariayat(reference)
    URLayat = "http://api.alquran.cloud/ayah"+reference
    r = requests.get(URLayat)
    data = r.json()
    
    if 'error' not in data:
        nom = data['data']['number']
        text = data['data']['text']

        iden = data['data']['edition']['identifier']
        langu = data['data']['edition']['language']
        name = data['data']['edition']['name']
        engnem = data['data']['edition']['englishName']
        frmt = data['data']['edition']['format']
        tip = data['data']['edition']['type']
        
        num = data['data']['surah']['number']
        nem = data['data']['surah']['name']
        englishName = data['data']['surah']['englishName']
        engnemtran = data['data']['surah']['englishNameTranslation']
        numofay = data['data']['surah']['numberOfAyahs']
        rt = data['data']['surah']['revelationType']

        data= "Nama_Surat : "+englishName+"\nsuratke- : "+num+"\nAyatke- : "+numofay
        return data
        
        # numinsurah = data['data']
        # juz = data['data']['juz']
        # manzil = data['data']['manzil']
        # page = data['data']['page']
        # ruku = data['data']['ruku']
        # hiz = data['data']['hizQuarter']
        # sajda = data['data']['sajda']

        if 'error' in data:
        err = data['error']
        print(err)

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
    if(data[0]=='view_surat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carisurat(data[1])))
    elif(data[0]=='view_ayat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cariayat(data[1]))
    elif(data[0]=='view_ayatrandom'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=cariayatrandom()))
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

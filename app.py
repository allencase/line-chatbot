from __future__ import unicode_literals
import os
from urllib.parse import parse_qsl
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
#from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    MessageTemplateAction,
    ImageSendMessage)

import configparser

import random
import json
app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
#print("channel_access_token",config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
#print("channel_secret",config.get('line-bot', 'channel_secret'))
# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    
    try:
        print("start:",body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route("/ok", methods=['GET'])
def ok():
    return 'OK'
@handler.add(PostbackEvent)
def handle_postback(event):
    # print(event.postback.data)
    # print(parse_qsl(event.postback.data))
    # print(dict(parse_qsl(event.postback.data)))
    data=dict(parse_qsl(event.postback.data))
    print(data)    
    if data['action'] == "product":
        title=data['title']
        price=str(data['price'])
        columns=[]
                    
        item=CarouselColumn(
                        thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t39.30808-1/327308531_562895052420678_8212018919637295467_n.png?_nc_cat=101&ccb=1-7&_nc_sid=c6021c&_nc_ohc=ZGEHUZMpMDAAX-kTXnk&_nc_ht=scontent.ftpe8-2.fna&oh=00_AfA-3lW5r55leF7VmL21fpNkWO9GVWbNj4f4fwjVsjj6eQ&oe=63D90363',
                        title=title,
                        text='請選擇甜度:',
                        actions=[
                                PostbackAction(
                                    label='全糖',
                                    display_text='全糖',
                                    data='action=sugar&sugar=全糖&title='+title+'&price='+price
                                ),
                                    PostbackAction(
                                    label='少糖',
                                    display_text='少糖',
                                    data='action=sugar&sugar=少糖&title='+title+'&price='+price
                                ),
                                    PostbackAction(
                                    label='半糖',
                                    display_text='半糖',
                                    data='action=sugar&sugar=半糖&title='+title+'&price='+price
                                ),                            
                                ]
                    )
        columns.append(item)
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=columns
            )
        )

        line_bot_api.reply_message(event.reply_token, carousel_template_message)       
    elif data['action'] == "sugar":
        title=data['title']
        price=str(data['price'])
        sugar=str(data['sugar'])
        columns=[]                    
        item=CarouselColumn(
                        thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t39.30808-1/327308531_562895052420678_8212018919637295467_n.png?_nc_cat=101&ccb=1-7&_nc_sid=c6021c&_nc_ohc=ZGEHUZMpMDAAX-kTXnk&_nc_ht=scontent.ftpe8-2.fna&oh=00_AfA-3lW5r55leF7VmL21fpNkWO9GVWbNj4f4fwjVsjj6eQ&oe=63D90363',
                        title=title,
                        text='請選擇是否加冰塊:',
                        actions=[
                                PostbackAction(
                                    label='正常',
                                    display_text='正常',
                                    data='action=ice&ice=正常&title='+title+'&price='+price+'&sugar='+sugar
                                ),
                                    PostbackAction(
                                    label='少冰',
                                    display_text='少冰',
                                    data='action=ice&ice=少冰&title='+title+'&price='+price+'&sugar='+sugar
                                ),
                                    PostbackAction(
                                    label='無冰',
                                    display_text='無冰',
                                    data='action=ice&ice=無冰&title='+title+'&price='+price+'&sugar='+sugar
                                ),                            
                                ]
                    )
        columns.append(item)
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=columns
            )
        )

        line_bot_api.reply_message(event.reply_token, carousel_template_message)       
    elif data['action'] == "ice":
        title=data['title']+"\r\n甜度:"+data['sugar']+"\r\n是否加冰塊:"+data['ice']
        price=str(data['price'])
        sugar=data['sugar']
        ice=data['ice']
        columns=[]                    
        item=CarouselColumn(
                        thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t39.30808-1/327308531_562895052420678_8212018919637295467_n.png?_nc_cat=101&ccb=1-7&_nc_sid=c6021c&_nc_ohc=ZGEHUZMpMDAAX-kTXnk&_nc_ht=scontent.ftpe8-2.fna&oh=00_AfA-3lW5r55leF7VmL21fpNkWO9GVWbNj4f4fwjVsjj6eQ&oe=63D90363',
                        title=title,
                        text='請確認你訂的項目',
                        actions=[
                                PostbackAction(
                                    label='正確',
                                    display_text='正確',
                                    data='action=ok&title='+title+'&price='+price+'&sugar='+sugar+'&ice='+ice
                                ),
                                    PostbackAction(
                                    label='重新訂購',
                                    display_text='重新訂購',
                                    data='action=menu'
                                ),                                                          
                                ]
                    )
        columns.append(item)
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=columns
            )
        )

        line_bot_api.reply_message(event.reply_token, carousel_template_message)       
    elif data['action'] == "ok":
        price=str(data['price'])
        sugar=data['sugar']
        ice=data['ice']
        title=data['title']
        pretty_text="謝謝你的訂購"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )
    elif data['action'] == "menu":
        pretty_echo(event)   
    
# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
 
    print("event",event)
    if event.source.user_id != "U6de72db2a466e3ae7b4326501c67a71b":      
        pretty_text="菜單:\r\n"
        with open('setup.json', encoding='utf-8') as json_file:
            setup = json.load(json_file)   
       
        columns=[]
        for json_item in setup['data']:                
            item=CarouselColumn(
                            thumbnail_image_url='https://scontent.ftpe8-2.fna.fbcdn.net/v/t39.30808-1/327308531_562895052420678_8212018919637295467_n.png?_nc_cat=101&ccb=1-7&_nc_sid=c6021c&_nc_ohc=ZGEHUZMpMDAAX-kTXnk&_nc_ht=scontent.ftpe8-2.fna&oh=00_AfA-3lW5r55leF7VmL21fpNkWO9GVWbNj4f4fwjVsjj6eQ&oe=63D90363',
                            title=json_item['title']+" ("+str(json_item['price'])+")",
                            text=json_item['title'],
                            actions=[
                                 PostbackAction(
                                    label='購買',
                                    display_text=json_item['title'],
                                    data='title='+json_item['title']+" ("+str(json_item['price'])+")"+'&price='+str(json_item['price'])+'&action=product'
                                ),
                            ]
                        )
            columns.append(item)
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=columns
            )
        )

        line_bot_api.reply_message(event.reply_token, carousel_template_message)
     

if __name__ == "__main__":
    app.run(debug=True)

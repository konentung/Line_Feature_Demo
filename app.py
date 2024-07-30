from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    StickerMessage,
    ImageMessage,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    ImagemapMessage,
    ImagemapArea,
    ImagemapBaseSize,
    ImagemapExternalLink,
    ImagemapVideo,
    URIImagemapAction,
    MessageImagemapAction,
    FlexMessage,
    FlexContainer,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    ImageCarouselTemplate,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    CarouselColumn,
    ImageCarouselColumn,
    QuickReply,
    QuickReplyItem
)
import line_flex
import os

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
    
line_handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

@app.route("/")
def index():
    return "2024 LineBot Building & Learning Behavior Analysis Workshop"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_messsage(event):
    message = event.message.text
    url_root = request.url_root.replace("http", "https")
    if message == "主選單":
        flex_json = line_flex.main_line_flex_str()
        reply_message(event, [FlexMessage(alt_text=message, contents=FlexContainer.from_json(flex_json))])
    elif message == "Action Types":
        flex_json = line_flex.actions_line_flex_str()
        reply_message(event, [FlexMessage(alt_text=message, contents=FlexContainer.from_json(flex_json))])
    elif message == "Message Types":
        flex_json = line_flex.messages_line_flex_str()
        reply_message(event, [FlexMessage(alt_text=message, contents=FlexContainer.from_json(flex_json))])
    elif message == "Template message":
        flex_json = line_flex.template_line_flex_str()
        reply_message(event, [FlexMessage(alt_text=message, contents=FlexContainer.from_json(flex_json))])
    elif message == "Flex message":
        flex_json = line_flex.flex_line_flex_str()
        reply_message(event, [FlexMessage(alt_text=message, contents=FlexContainer.from_json(flex_json))])
    elif message == "Text message":
        reply_message(event, [TextMessage(text="Text message")])
    elif message == "Sticker message":
        reply_message(event, [StickerMessage(package_id="446", sticker_id="1988")])
    elif message == "Image message":
        url = f"{url_root}/static/logo.png"
        app.logger.info(url)
        # reply_message(event, [ImageMessage(original_content_url=url, preview_image_url=url)])
        reply_message(event, [TextMessage(text=url)])
    elif message == "Video message":
        url = f"{url_root}static/video.mp4"
        reply_message(event, [VideoMessage(original_content_url=url, preview_image_url=url)])
    elif message == "Audio message":
        url = f"{url_root}static/music.mp3"
        reply_message(event, [AudioMessage(original_content_url=url, duration=60000)])
    elif message == "Location message":
        reply_message(event, [LocationMessage(title='Location', address="Taipei", latitude=25.0475, longitude=121.5173)])
    elif message == "Imagemap message":
        reply_message(event, [                    
            ImagemapMessage(
                base_url=f"{url_root}static/imagemap",
                alt_text='this is an imagemap',
                base_size=ImagemapBaseSize(height=1040, width=1040),
                video=ImagemapVideo(
                    original_content_url=f"{url_root}static/video.mp4",
                    preview_image_url=f"{url_root}static/preview_image.png",
                    area=ImagemapArea(
                        x=0, y=0, width=1040, height=520
                    ),
                    external_link=ImagemapExternalLink(
                        link_uri='https://www.youtube.com/@bigdatantue',
                        label='點我看更多',
                    ),
                ),
                actions=[
                    URIImagemapAction(
                        type = "uri",
                        linkUri='https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y=',
                        area=ImagemapArea(
                            x=0, y=520, width=520, height=520
                        )
                    ),
                    MessageImagemapAction(
                        type ="message",
                        text='這是fb網頁https://www.facebook.com/NTUEBIGDATAEDU',
                        area=ImagemapArea(
                            x=520, y=520, width=520, height=520
                        )
                    )
                ]
            )
        ])
    elif message == "Confirm Template":
        confirm_template = ConfirmTemplate(
            text='訂閱追蹤國北教大教育大數據了嗎?',
            actions=[
                MessageAction(label='是', text='是!'),
                MessageAction(label='否', text='否!')
            ]
        )
        reply_message(event, [TemplateMessage(alt_text='Confirm Template', template=confirm_template)])
    elif message == "Button Template":
        buttons_template = ButtonsTemplate(
                thumbnail_image_url= f"{url_root}static/Logo.png",
                title='相關社群連結',
                text='教育大數據的社群連結',
                actions=[
                    URIAction(label='教育大數據微學程FB連結', uri='https://www.facebook.com/NTUEBIGDATAEDU'),
                    URIAction(label='教育大數據微學程YT連結', uri='https://www.youtube.com/@bigdatantue'),
                    URIAction(label='教育大數據微學程IG連結', uri='https://www.instagram.com/ntue.bigdata')
                ]
            )
        reply_message(event, [TemplateMessage(alt_text="Buttom Template", template=buttons_template)])
    elif message == "Carousel Template":
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=f"{url_root}static/FB.png",
                    title='Facebook',
                    text='大數據教育微學程FB粉絲專頁',
                    actions=[
                        URIAction(
                            label='按我前往Facebook',
                            uri='https://www.facebook.com/NTUEBIGDATAEDU'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=f"{url_root}static/YT.png",
                    title='Youtube',
                    text='大數據教育微學程Youtube頻道',
                    actions=[
                        URIAction(
                            label='按我前往Youtube',
                            uri='https://www.youtube.com/@bigdatantue'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url=f"{url_root}static/IG.png",
                    title='Instagram',
                    text='大數據教育微學程Instagram帳號',
                    actions=[
                        URIAction(
                            label='按我前往 Instagram',
                            uri='https://www.instagram.com/ntue.bigdata'
                        )
                    ]
                )
            ]
        )
        reply_message(event, [TemplateMessage(alt_text='Carousel Template', template=carousel_template)])
    elif message == "Image Carousel Template":
        image_carousel_template = ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url=f"{url_root}static/facebook.png",
                    action=URIAction(
                        label='造訪FB',
                        uri='https://www.facebook.com/NTUEBIGDATAEDU'
                    )
                ),
                ImageCarouselColumn(
                    image_url=f"{url_root}static/youtube.png",
                    action=URIAction(
                        label='造訪YT',
                        uri='https://www.youtube.com/@bigdatantue'
                    )
                ),
                ImageCarouselColumn(
                    image_url=f"{url_root}static/instagram.png",
                    action=URIAction(
                        label='造訪IG',
                        uri='https://www.instagram.com/ntue.bigdata'
                    )
                )                
            ]
        )
        reply_message(event, [TemplateMessage(alt_text='Image Carousel Template', template=image_carousel_template)])
    elif message == "Line Flex Message":
        flex_json = line_flex.scedule_line_flex_str()
        reply_message(event, [FlexMessage(alt_text=message, contents=FlexContainer.from_json(flex_json))])
    elif message == "Quick Reply":
        quick_reply = TextMessage(
            text='請選擇項目',
            quick_reply=QuickReply(
                items=[
                    QuickReplyItem(
                        action=PostbackAction(
                            label="Postback",
                            data="Postback"
                        )
                    ),
                    QuickReplyItem(
                        action=MessageAction(
                            label="Message",
                            text="message"
                        )
                    ),
                    QuickReplyItem(
                        action=URIAction(
                            label="URI",
                            uri="https://www.instagram.com/ntue.bigdata"
                        )
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Datetime Picker",
                            data="datetimepicker",
                            mode="datetime"
                        )
                    ),
                    QuickReplyItem(
                        action=CameraAction(label="Camera")
                    ),
                    QuickReplyItem(
                        action=CameraRollAction(label="Camera Roll")
                    ),
                    QuickReplyItem(
                        action=LocationAction(label="Location")
                    )
                ]
            )
        )
        reply_message(event, [quick_reply])
    else:
        reply_message(event, [TextMessage(text=message)])

@line_handler.add(FollowEvent)
def handle_follow(event):
    reply_message(event, [TextMessage(text="歡迎加入我們的工作坊Line Bot")])
    
@line_handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == "Postback":
        raw_body = request.get_data(as_text=True)
        reply_message(event, [TextMessage(text=raw_body)])
    elif event.postback.data == "datetimepicker":
        raw_body = request.get_data(as_text=True)
        reply_message(event, [TextMessage(text=raw_body)])
    else:
        reply_message(event, [TextMessage(text=event.postback.data)])

def reply_message(event, messages):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=messages
            )
        )
    
if __name__ == "__main__":
    app.run()
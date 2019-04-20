# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)

import credentials
import geniusLyrics

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = credentials.LINE_Secret
channel_access_token = credentials.LINE_AccessToken #ここも変えて
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


# def test():
#     print(geniusLyrics.test())
    # geniusLyrics.songInformation("lemon","")
    # print("hellos")
    # response= geniusLyrics.songInformation("lemon","yonedu")
    # json = response.json()
    # print(json)
    #
    # remote_song_info = None

@app.route("/callback", methods=['POST'])
def callback():
    # test()
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
def message_text(event):
    searchtext = event.message.text
    language_list = geniusLyrics.songInformation(searchtext)

    # print(searchtext)
    if( ":" in searchtext):
        url = geniusLyrics.getUrl(language_list[0])
        lyrics = geniusLyrics.getLyricstext(url)
        # print(lyrics)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=lyrics) )
        return
    elif searchtext == "ごめんなかった":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Sorry") )
        return

    items = [QuickReplyButton(action=MessageAction(label=f"{language}", text=f"{language}")) for language in language_list]

    messages = TextSendMessage(text="曲を選んで",
                               quick_reply=QuickReply(items=items))

    line_bot_api.reply_message(event.reply_token, messages=messages)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

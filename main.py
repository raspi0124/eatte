from flask import Flask, request, abort
import dateutil.parser as dparser
from dateutil import relativedelta
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)
import configparser
from datetime import datetime, date, timedelta

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('../eatte.setting')

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = config.get("dev", "YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET = config.get("dev", "YOUR_CHANNEL_SECRET")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
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

@app.route("/", methods=['GET'])
def top():
	abort(404)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	today = datetime.today()
	tomorrow = today + timedelta(days=1)
	if "明日" in event.message.text:
		date = datetime.strftime(tomorrow, '%m月%d日')
	if "今日" in event.messsage.text:
		date = datetime.strftime(today, '%m月%d日')
	else:
		try:
			rawdate = dparser.parse(event.message.text,fuzzy=True)
			date = rawdate.strftime('%m月%d日')
		except dparser._parser.ParserError:
			else:
				return ""
	if "欠席" in event.message.text or "休む" in event.message.text or "行かない" in event.message.text or "行けない" in event.message.text and date is not None:
		reptext = "" + date + " に欠席?おっけー。"
	if "出席" in event.message.text or "行く" in event.message.text and date is not None:
		reptext = "" + date + " に出席?了解。"
	if "遅れて" in event.message.text or "遅れる" in event.message.text or "遅刻" in event.message.text and date is not None:
		reptext = "" + date + " に遅れる?了解です。詳しいことはとりあえずこのbotまだ対応できないから部長らへんに言ってね!"
	#elif
	#	reptext = "日付は認識しましたが何を言ってるのかを認識できませんでした。。日付と一緒に'遅刻'、'行く'、'休む'等のキーワードを入れてね!"
	print(event.message.text)
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=reptext))


if __name__ == "__main__":
#    app.run()
	port = 80
	app.run(host="0.0.0.0", port=port)

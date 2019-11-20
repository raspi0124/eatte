import gspread
import json

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('../eattecred.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1QHGeSZRFmh2vyj8nKbbwcjdCXKZWvs_Sms8mS6l0_KE'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).get_worksheet(0)

def getlistofpeople():
	raw_col_list = worksheet.col_values(1)
	#raw_col_list.pop(0)
	return raw_col_list
def getlistofdate():
	raw_row_list = worksheet.row_values(1)
	#Same reason here as getlistofpeople()
	#raw_row_list.pop(0)
	return raw_row_list
def searchthing(tosearch, list):
	#TODO:後で見つからなかった際のreturnも追加
	num = list.index(str(tosearch))
	return num
def addpeople(name):
	name = str(name)
	worksheet.append_row([name])
	return True
def ispeopleexist(name):
	aa = getlistofpeople()
	if name in aa:
		return True
	else:
		return False
def isdateexist(date):
	aa = getlistofdate()
	if date in aa:
		return True
	else:
		return False
def adddate(date):
	date = str(date)
	list = getlistofdate()
	if date in list:
		return None
	else:
		num = int(len(list))
		num += 1
		worksheet.update_cell("1", num, date)
		return True
def updateattendance(name, date, status):
	if ispeopleexist(name):
		pass
	else:
		addpeople(name)
	if isdateexist(date):
		pass
	else:
		adddate(date)
	nameplace = int(searchthing(name, getlistofpeople()))
	dateplace = int(searchthing(date, getlistofdate()))
	nameplace = nameplace + 1
	dateplace = dateplace + 1
	str(status)
	worksheet.update_cell(nameplace, dateplace, status)
	#TODO:ここらへんにrowが無かった場合の対応書く?

def marklate(name, date):
	updateattendance(name, date, "Late")
def marknotgoing(name, date):
	updateattendance(name, date, "Not going")
def markgoing(name, date):
	updateattendance(name, date, "Going")

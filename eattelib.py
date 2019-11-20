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
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

def getlistofpeople():
	raw_row_list = worksheet.row_values(1)
	#最初のelementを除くことでラベルを削除
	parsedlist = raw_row_list.pop(0)
	return parsedlist
def getlistofdate():
	raw_col_list = worksheet.col_values(1)
	#Same reason here as getlistofpeople()
	parsedlist = raw_col_list.pop(0)
	return parsedlist
def searchthing(tosearch, list):
	#TODO:後で見つからなかった際のreturnも追加
	num = list.index(str(tosearch))
	return num
def addpeople(name):
	name = str(name)
	worksheet.append_row([name])
	return True
#def adddate(date):
#	date = str(date)
#	worksheet.append_col([date])
#def updateattendance(name, date):
#	nameplace = searchthing(name, getlistofpeople())
#	dateplace = searchthing(date, getlistofdate())
	#TODO:ここらへんにrowが無かった場合の対応書く?
	

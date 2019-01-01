import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('aaaaaaaaaaaaa.json', scope)

gc = gspread.authorize(credentials)
aug_sheet = gc.open('THFInformation').worksheet("AugList")
info_sheet = gc.open('THFInformation').worksheet("Python")

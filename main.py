import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('meta-credecntials.json', scope)

gc = gspread.authorize(credentials)
lib_sheet = gc.open('Game Library').worksheet("Full Library")
info_sheet = gc.open('Game Library').worksheet("Python")

# Take URL with bs and check MC values


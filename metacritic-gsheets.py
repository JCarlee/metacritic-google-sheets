import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import Request, urlopen


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('meta-credentials.json', scope)

gc = gspread.authorize(credentials)
lib_sheet = gc.open('Game Library').worksheet("Library")
info_sheet = gc.open('Game Library').worksheet("Python")

start_row = info_sheet.acell('A2').value
end_row = info_sheet.acell('B2').value

# Create List from Games
game_list = []
# Create List from Platforms
plat_list = []

for game, platform in zip(game_list, plat_list):
    req = Request('https://www.metacritic.com/game/xbox-one/red-dead-redemption-2', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    name_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
    box = name_box.text.strip()
    print(box)



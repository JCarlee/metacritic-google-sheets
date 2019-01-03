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
base_url = 'https://www.metacritic.com/game/'


# Create List of games
games = []
game_cells = lib_sheet.range('A' + start_row + ':A' + end_row)
for cell_val in game_cells:
    games.append(cell_val.value.replace(' ', '-').lower())

# Create list of platforms
plat_list = []
plat_cells = lib_sheet.range('B' + start_row + ':B' + end_row)
for cell_val in plat_cells:
    plat_list.append(cell_val.value.replace(' ', '-').lower())

for n, i in enumerate(plat_list):
    if i == 'steam' or i == 'uplay':
        plat_list[n] = 'pc'


for game, platform in zip(games, plat_list):
    current_url = base_url + platform + '/' + game
    print(current_url)
    req = Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, features="html.parser")
    name_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
    box = name_box.text.strip()
    print(box)

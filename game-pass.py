import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import Request, urlopen

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('meta-credentials.json', scope)
gc = gspread.authorize(credentials)
lib_sheet = gc.open('Game Library').worksheet("GamePass")
info_sheet = gc.open('Game Library').worksheet("Python")

row_end = info_sheet.acell('D2').value
base_url = 'https://www.metacritic.com/game/'


# Create List of games
games = []
game_cells = lib_sheet.range('A2:A' + row_end)
for cell_val in game_cells:
    games.append(cell_val.value.replace(' ', '-').lower())


# list of scores taken from spreadsheet
score_list = lib_sheet.range('B2:B' + row_end)

# main loop to perform essential tasks
for game, cell in zip(games, score_list):
    current_url = base_url + 'xbox-360/' + game
    try:
        if cell.value == '':
            req = Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, features="html.parser")
            name_box = soup.find('span', attrs={'itemprop': 'ratingValue'})
            box = name_box.text.strip()
            cell.value = box
    except:
        print(current_url + ' not read')

lib_sheet.update_cells(score_list)

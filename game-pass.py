import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import Request, urlopen

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('meta-credentials.json', scope)
gc = gspread.authorize(credentials)
gp_sheet = gc.open('Game Library').worksheet("GamePass")
info_sheet = gc.open('Game Library').worksheet("Python")

gp_row_end = info_sheet.acell('B2').value
base_url = 'https://www.metacritic.com/game/'

gp_game_list = []
gp_game_cells = gp_sheet.range('A2:A' + gp_row_end)
for cell_val in gp_game_cells:
    gp_game_list.append(cell_val.value.replace(' ', '-').lower())

gp_plat_cells = gp_sheet.range('B2:B' + gp_row_end)
gp_score_list = gp_sheet.range('C2:C' + gp_row_end)

# Add platform values if don't exist
for game, plat_cell in zip(gp_game_list, gp_plat_cells):
    current_url = base_url + 'xbox360/' + game
    try:
        if plat_cell.value == '':
            req = Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            plat_cell.value = 'Xbox 360'
    except:
        plat_cell.value = 'Xbox One'

gp_sheet.update_cells(gp_plat_cells)

gp_plat_list = []
for plat_cell_val in gp_plat_cells:
    gp_plat_list.append(plat_cell_val.value.replace(' ', '-').lower())


# Metacritic score
for game, platform, cell in zip(gp_game_list, gp_plat_list, gp_score_list):
    current_url = base_url + platform + '/' + game
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
gp_sheet.update_cells(gp_score_list)

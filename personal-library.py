import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import Request, urlopen

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('meta-credentials.json', scope)
gc = gspread.authorize(credentials)
lib_sheet = gc.open('Game Library').worksheet("Library")
gp_sheet = gc.open('Game Library').worksheet("GamePass")
info_sheet = gc.open('Game Library').worksheet("Python")

lib_row_end = info_sheet.acell('A2').value
base_url = 'https://www.metacritic.com/game/'

lib_game_list = []
lib_game_cells = lib_sheet.range('A2:A' + lib_row_end)
for cell_val in lib_game_cells:
    lib_game_list.append(cell_val.value.replace(' ', '-').lower())

lib_platform_list = []
plat_cells = lib_sheet.range('B:B' + lib_row_end)
for cell_val in plat_cells:
    lib_platform_list.append(cell_val.value.replace(' ', '-').lower())

pc_platforms = ['steam', 'uplay', 'epic-launcher', 'origin', 'gog']
for n, i in enumerate(lib_platform_list):
    if i in pc_platforms:
        lib_platform_list[n] = 'pc'

# list of scores taken from spreadsheet
lib_score_list = lib_sheet.range('C2:C' + lib_row_end)

# main loop to perform essential tasks
for game, platform, cell in zip(lib_game_list, lib_platform_list, lib_score_list):
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

lib_sheet.update_cells(lib_score_list)

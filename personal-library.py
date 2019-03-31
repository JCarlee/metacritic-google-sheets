import gspread
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import Request, urlopen

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('meta-credentials.json', scope)
gc = gspread.authorize(credentials)

lib_sheet = gc.open('Game Library').worksheet("Library")
info_sheet = gc.open('Game Library').worksheet("Python")

base_url = 'https://www.metacritic.com/game/'
lib_row_end = info_sheet.acell('A2').value
game_cells = lib_sheet.range('A2:A' + lib_row_end)
platform_cells = lib_sheet.range('B2:B' + lib_row_end)
score_list = lib_sheet.range('C2:C' + lib_row_end)
pc_platforms = ['steam', 'uplay', 'epic-launcher', 'origin', 'gog']


def create_process_lists():
    game_list = []
    platform_list = []
    for cell_val in game_cells:
        game_list.append(cell_val.value.replace(' ', '-').lower())

    for cell_val in platform_cells:
        platform_list.append(cell_val.value.replace(' ', '-').lower())

    for n, i in enumerate(platform_list):
        if i in pc_platforms:
            platform_list[n] = 'pc'
    return game_list, platform_list


def process(i, j):
    for game, platform, cell in zip(i, j, score_list):
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
            if current_url != 'https://www.metacritic.com/game//':
                print(current_url + ' not read')
    lib_sheet.update_cells(score_list)


a, b = create_process_lists()
process(a, b)

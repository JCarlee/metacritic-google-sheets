# Metacritic Google Sheets
Write Metacritic scores to game libraries in Google Sheets.

## Motivation
I wrote these scripts to help prioritize my gaming backlog by listing Metacritic score with all games in my library as well as all Xbox Game Pass games. Finding nothing online that completed this task, I decided to create a very simple implementation using Python and Google Sheets.

I consider myself a novice Python developer so I invite any and all criticism to the approach, code, and documentation. Please feel free to email me at JCarlee@gmail.com with suggestions or ideas.

## Dependencies
* Python 3
* BeautifulSoup (bs4)
* gspread
* urllib
* oauth2client.service_account
```
pip install bs4
pip install gspread
pip install urllib
pip install oauth2client
```
## Google Sheets Setup Credentials
Coming Soon

## game-pass.py
* Uses a Google Spreadsheet library of Xbox Game Pass games to update the Metacritic score of said games using BeautifulSoup.
* Because Game Pass encompasses Xbox One and Xbox 360 backwards compatible games, there is a built in check to define this in the spreadsheet.
```python
for game, plat_cell in zip(gp_game_list, gp_plat_cells):
    current_url = base_url + 'xbox360/' + game
    try:
        if plat_cell.value == '':
            req = Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            plat_cell.value = 'Xbox 360'
    except:
        plat_cell.value = 'Xbox One'
```

## personal-library.py
* Provides metacritic score updates to my personal game library
* Handles various platform types including Xbox One, Xbox 360, uPLAY, and Steam

## Author

* **John Carlee** - JCarlee@gmail.com

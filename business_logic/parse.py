import requests
from bs4 import BeautifulSoup
import json

url = "https://fcnn.ru/season/championship/stat"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

players = []

for row in soup.select('table tr'):
    cols = row.find_all('td')
    if len(cols) >= 12:  # 12 колонок: #, имя, позиция, и, ип, бз, вз, вбз, г, ПАС, п, у
        # Чистим дубли в имени
        name = ' '.join(cols[1].get_text(strip=True).split())
        player = {
            'number': cols[0].get_text(strip=True),
            'name': name,
            'position': cols[2].get_text(strip=True),
            'matches': cols[3].get_text(strip=True),           # и
            'full_games': cols[4].get_text(strip=True),        # ип
            'was_replaced': cols[5].get_text(strip=True),      # бз
            'came_replace': cols[6].get_text(strip=True),      # вз
            'was_and_came_replace': cols[7].get_text(strip=True), # вбз
            'goals': cols[8].get_text(strip=True),            # г
            'assists': cols[9].get_text(strip=True),          # ПАС
            'yellow_cards': cols[10].get_text(strip=True),    # п
            'red_cards': cols[11].get_text(strip=True),       # у
            'image': cols[1].find('img')['src'] if cols[1].find('img') else None
        }
        players.append(player)

# Сохраняем в JSON
with open('players.json', 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=False, indent=4)

print(f"Сохранили {len(players)} игроков в players.json")

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time

aktualni_slozka = os.getcwd()   # určuju kde mám aktuální složku ve které programuju
vysledne_csv = os.path.join(aktualni_slozka, "csfd_top_500.csv")     # výsledný soubor se má uložit do té složky

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

seznam_filmu = []

# Chceme 5 stránek po 100 filmech, každá stránka má na konci adresy číslo (https://www.csfd.cz/zebricky/filmy/nejlepsi/?from=300)
stranky = [1, 100, 200, 300, 400, 500]

for start in stranky:
    if start == 1:
        URL = "https://www.csfd.cz/zebricky/filmy/nejlepsi/"
    else:
        URL = f"https://www.csfd.cz/zebricky/filmy/nejlepsi/?from={start}"

    print (f"právě stahuji: {URL}")

    # Začíná scrapování
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    filmy = soup.find_all('article', class_ = 'article')
    
    for f in filmy:
        try:
            # Název
            nazev_tag = f.find('a', class_='film-title-name')
            if not nazev_tag: continue #Pokud název nejadeš, přeskoč ho
            nazev = nazev_tag.text.strip()

            # Hodnocení
            hodnoceni_raw = f.find('div', class_= 'rating-average').text.strip()
            hodnoceni = float(hodnoceni_raw.replace('%', '').replace(',', '.'))
            # Místo 95,4% (text) budu mít 95.4 (číslo)

            # Rok
            info_tag = f.find('span', class_= 'info')
            rok_match = re.search(r'\d{4}', info_tag.text) if info_tag else None
            rok = int(rok_match.group()) if rok_match else 0

            seznam_filmu.append({
                "Rank": len(seznam_filmu) + 1,
                "Title": nazev,
                "Rating": hodnoceni,
                "Year": rok
            })

        except:
            continue

time.sleep(5) # po každém stažení stránky se počká 5 sekund

# Uložení
df = pd.DataFrame(seznam_filmu)
df.to_csv(vysledne_csv, index=False, encoding="utf-8-sig")

print(f"HOTOVO! Celkem v seznamu: {len(seznam_filmu)} filmů.")
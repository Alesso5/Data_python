import requests
from bs4 import BeautifulSoup
import pandas as pd
import re #pro čistější čistění
import os

URL = "https://www.csfd.cz/zebricky/filmy/nejlepsi/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

# Zkusíme poslat požadavek na  server
response = requests.get(URL, headers=headers)
# Ověření, jestli je stavový kód 200 (OK)
#print(f"stavový kód: {response.status_code}")

# Najít všechny články o filmech
soup = BeautifulSoup(response.content, 'html.parser')
filmy = soup.find_all('article', class_ = 'article')
# Ověřit, kolik boxů s filmy našla Soup na stránce
#print(f"Našla jsem celkem {len(filmy)}")

# Vypíšeme si kousek HTML kódu, abychom viděli, co že to máme
#print("Obsah prvního filmu")
#print(filmy[0].prettify()[:1000])  # vypíše prvních 1000 znaků HTML

# Dolování dat z jednoho filmu
prvni_film = filmy[0]

# 1. NÁZEV - třída film-title-name   tag a
nazev_tag = prvni_film.find('a', class_='film-title-name')
nazev = nazev_tag.text.strip() if nazev_tag else "Název nenalezen"  # oříznu mezery před a za textem, ošetřím chybu když název filmu nebude
#print(nazev)

# 2. HODNOCENÍ - třída rating-average  tag div
hodnoceni_tag = prvni_film.find('div', class_= 'rating-average')
hodnoceni = hodnoceni_tag.text.strip() if hodnoceni_tag else "0%"
#print(hodnoceni)

# 3. ROK třída info tag span
info_tag = prvni_film.find('span', class_= 'info')
rok_text = info_tag.text.strip() if info_tag else ""
#print(rok_text)

# Použití regulárního výrazu pro odstranění závorek
match = re.search(r'\d{4}', rok_text)  # odstraní závorky a nechá jen čísla
rok = match.group() if match else "????"
#print(rok)


# SMYČKA PRO VŠECHNY FILMY
seznam_filmu = []

for f in filmy:
    try:
        # Název
        nazev_tag = f.find('a', class_='film-title-name')
        if not nazev_tag: continue #Pokud název nejadeš, přeskoč ho
        nazev = nazev_tag.text.strip()

        # Hodnocení (očistit od % a čárky, aby to bylo číslo)
        hodnoceni_raw = f.find('div', class_= 'rating-average').text.strip()
        hodnoceni = hodnoceni_raw.replace('%', '').replace(',', '.')
        # Místo 95,4% (text) budu mít 95.4 (číslo)

        # Rok
        info_tag = f.find('span', class_= 'info')
        rok_match = re.search(f'\d{4}', info_tag.text) if info_tag else None
        rok = rok_match.group() if rok_match else 0
        # Místo (1994) mám 1994, takže pak ve streamůlitu můžu filtrovat a počítat nebo dělat graf podle let

        seznam_filmu.append({
            "Rank": len(seznam_filmu) +1,
            "Title": nazev,
            "Rating": float(hodnoceni),
            "Year": int(rok)
        })

    except Exception as e:
        continue
        # POkud narazíš na chybu, ignoruj jí a pokračuj dál

#print(seznam_filmu)

# Cesta k výslednému souboru
vysledne_csv = os.path.join('csfd_top_100.csv')

# Uložení do CSV
df = pd.DataFrame(seznam_filmu)
df.to_csv(vysledne_csv, index=False, encoding="utf-8-sig")

# Printy a kontrola
print(f"HOTOVO! Našel jsem {len(seznam_filmu)} filmů.")
print(f"Soubor 'csfd_top_100.csv' byl vytvořen ve složce")



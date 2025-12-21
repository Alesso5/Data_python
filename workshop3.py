# Přejmenovat sloupce aby byly hezky česky
# Výpočet dekády - z které dekády film pochází
# Podle hodnocení rozdělit filmy kultovní pecky - skvělé filmy - ostatní

import pandas as pd
import os

# 1. Nastavení cest
aktualni_slozka = os.getcwd()
vstupni_csv = os.path.join(aktualni_slozka, "csfd_top_500.csv" )

# 2. Načtení dat
df = pd.read_csv(vstupni_csv)
#print(df)

# 3. Přejmenování sloupců
df = df.rename(columns={
    "Rank": "poradi",
    "Title": "nazev",
    "Rating": "hodnoceni",
    "Year": "rok"
})
#print(df)

# Výpočet dekády
# operátor // modulo pro celočíselné dělení. (1994 // 10) je 199. 199*10 = 1990
df['dekada'] = (df['rok'] // 10) * 10
#print(df)

# Tvorba kategorie podle hodnocení
def urci_kategorii(body):
    if body>=90:
        return "Kultovní pecka"
    elif body >=85:
        return "Vynikající"
    else:
        return "Velmi dobrý"

df['kategorie'] = df['hodnoceni'].apply(urci_kategorii)
#print(df)

# odstranění chyb - pokud jsme scrapnuli rok 0, vyhodíme ho
df = df[df['rok'] > 0]

# seřadíme hodnocení od největšího po nejmenší
df = df.sort_values(by='hodnoceni', ascending = False)
#print(df)

# uložení souboru
vystupní_csv = os.path.join(aktualni_slozka, "csfd_pro_streamlit.csv")
df.to_csv(vystupní_csv, index = False, encoding = "utf-8-sig")

print(f"Soubor 'csfd_pro_streamlit.csv' byl vytvořen ve složce")
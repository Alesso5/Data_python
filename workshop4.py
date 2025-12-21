import streamlit as st
import pandas as pd
import os

# Titulní nadpis
st.title("🎞️ Analýza nejlepších filmů ČSFD")
st.markdown("Tato aplikace zobrazuje data, získaná scrapováním žebříčku TOP 500 filmů")

aktualni_slozka = os.getcwd()
cesta_data = os.path.join(aktualni_slozka, "csfd_pro_streamlit.csv")

# POužijeme st.cache_data, aby se data nenačítala znovu při každém kliknut z githubu
@st.cache_data
def nacti_data():
    return pd.read_csv(cesta_data)
df = nacti_data()

# Vložení tabulky do streamlitu, abych viděla, že se mi to načetlo správně
#st.dataframe(df.head(10))

# Filtrování - sidebar
st.sidebar.header("Filtry")

# Filtrování - sidebar
st.sidebar.header("Filtry")

# Zjistíme nejstarší a nejmladší film v datech
min_rok = int(df['rok'].min())
max_rok = int(df['rok'].max())

# Vtvoříme posuvník do bočního panelu, kde se můžu přepínat mezi roky
vybrane_roky = st.sidebar.slider(
    "Vyber rozmezí let",
    min_rok,
    max_rok,
    (min_rok, max_rok)  # výchozí poloha (vše vybráno)
)

# Vytvoření tabulky, kterou napojíme na posuvník
df_filtrovane = df[df['rok'].between(vybrane_roky[0], vybrane_roky[1])]
#  zobrazení výsledků
st.subheader(f"Zobrazeno filmů: {len(df_filtrovane)}")
st.dataframe(df_filtrovane)

# Metriky - počet filmů, průměrné hodnocení, nejvyšší hodnocení
st.subheader("Statistický přehled výběru")
# vytvoříme sloupečky pro metriky
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Počet filmů", len(df_filtrovane))

with col2:
    # spořítám si průměrné hodnocení vybraných filmů
    avg_rating = df_filtrovane['hodnoceni'].mean()
    st.metric("Průměrné hodnocení", f"{avg_rating:.2f} %")

with col3:
    max_rating = df_filtrovane['hodnoceni'].max()
    st.metric("nejvyšší hodnocení", f"{max_rating} %")

# graf filmů podle dekád
st.subheader("🍾 Distribuce filmů podle dekád")
# Kolik filmů je v jaké dekádě
dekady_data = df_filtrovane['dekada'].value_counts().sort_index()
# zobrazení grafu ve streamlitu
st.bar_chart(dekady_data)


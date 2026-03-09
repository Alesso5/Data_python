import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="ČSFD TOP 500 Analýza",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Analýza nejlepších filmů ČSFD")
st.markdown("Interaktivní analýza TOP 500 filmů podle žebříčku ČSFD")

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def nacti_data():
    cesta = os.path.join(os.getcwd(), "csfd_pro_streamlit.csv")
    return pd.read_csv(cesta)

df = nacti_data()

# ── Sidebar filtry ────────────────────────────────────────────────────────────
st.sidebar.header("🎛️ Filtry")

min_rok, max_rok = int(df['rok'].min()), int(df['rok'].max())
vybrane_roky = st.sidebar.slider("Rozmezí let", min_rok, max_rok, (min_rok, max_rok))

kategorie_moznosti = ["Vše"] + sorted(df['kategorie'].unique().tolist())
vybrana_kategorie = st.sidebar.selectbox("Kategorie", kategorie_moznosti)

min_hodnoceni = st.sidebar.slider("Minimální hodnocení (%)", 
                                   float(df['hodnoceni'].min()), 
                                   float(df['hodnoceni'].max()), 
                                   float(df['hodnoceni'].min()))

hledany_nazev = st.sidebar.text_input("🔍 Hledat film")

# ── Filtrování ────────────────────────────────────────────────────────────────
df_f = df[df['rok'].between(vybrane_roky[0], vybrane_roky[1])]
df_f = df_f[df_f['hodnoceni'] >= min_hodnoceni]
if vybrana_kategorie != "Vše":
    df_f = df_f[df_f['kategorie'] == vybrana_kategorie]
if hledany_nazev:
    df_f = df_f[df_f['nazev'].str.contains(hledany_nazev, case=False, na=False)]

# ── Metriky ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("🎥 Počet filmů", len(df_f))
c2.metric("⭐ Průměrné hodnocení", f"{df_f['hodnoceni'].mean():.2f} %")
c3.metric("🏆 Nejvyšší hodnocení", f"{df_f['hodnoceni'].max()} %")
c4.metric("📅 Rozsah let", f"{int(df_f['rok'].min())} – {int(df_f['rok'].max())}" if len(df_f) else "–")

st.divider()

# ── Grafy ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Filmy podle dekády")
    dekady = df_f['dekada'].value_counts().sort_index().reset_index()
    dekady.columns = ['dekada', 'pocet']
    fig1 = px.bar(dekady, x='dekada', y='pocet', 
                  color='pocet', color_continuous_scale='Viridis',
                  labels={'dekada': 'Dekáda', 'pocet': 'Počet filmů'},
                  template='plotly_dark')
    fig1.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🥧 Rozložení kategorií")
    kat = df_f['kategorie'].value_counts().reset_index()
    kat.columns = ['kategorie', 'pocet']
    fig2 = px.pie(kat, names='kategorie', values='pocet',
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  template='plotly_dark', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Hodnocení v čase")
    fig3 = px.scatter(df_f, x='rok', y='hodnoceni', 
                      color='kategorie', hover_data=['nazev'],
                      labels={'rok': 'Rok', 'hodnoceni': 'Hodnocení (%)'},
                      template='plotly_dark',
                      color_discrete_sequence=px.colors.qualitative.Set1)
    fig3.update_traces(marker=dict(size=6, opacity=0.7))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🏅 TOP 10 filmů")
    top10 = df_f.nlargest(10, 'hodnoceni')[['nazev', 'hodnoceni', 'rok', 'kategorie']]
    fig4 = px.bar(top10.sort_values('hodnoceni'), 
                  x='hodnoceni', y='nazev', orientation='h',
                  color='hodnoceni', color_continuous_scale='RdYlGn',
                  labels={'hodnoceni': 'Hodnocení (%)', 'nazev': ''},
                  template='plotly_dark', range_x=[80, 100])
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Tabulka ───────────────────────────────────────────────────────────────────
st.subheader(f"🗂️ Tabulka filmů ({len(df_f)} výsledků)")
st.dataframe(
    df_f[['poradi', 'nazev', 'hodnoceni', 'rok', 'dekada', 'kategorie']].reset_index(drop=True),
    use_container_width=True,
    hide_index=True
)

st.caption("Data získána scrapováním žebříčku ČSFD TOP 500 · Projekt pro výukové účely")
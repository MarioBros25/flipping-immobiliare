
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# Carica i dati
@st.cache_data
def load_data():
    return pd.read_csv("mappa_flipping_viterbo.csv")

df = load_data()

# Sidebar - Filtri
st.sidebar.title("Filtri")
min_margine = st.sidebar.slider("Margine netto minimo (€)", min_value=-50000, max_value=100000, value=10000, step=5000)
min_superficie = st.sidebar.slider("Superficie minima (mq)", 40, 150, 60)
localita = st.sidebar.multiselect("Località", options=df["Località"].unique(), default=list(df["Località"].unique()))

# Applica filtri
filtro_df = df[(df["Margine Netto Stimato"] > min_margine) &
               (df["Superficie (mq)"] >= min_superficie) &
               (df["Località"].isin(localita))]

st.title("Opportunità di Flipping a Viterbo")
st.markdown(f"Visualizzazione di **{len(filtro_df)}** immobili con margine netto > €{min_margine}")

# Mappa
m = folium.Map(location=[42.42, 12.11], zoom_start=10)
marker_cluster = MarkerCluster().add_to(m)

for _, row in filtro_df.iterrows():
    if pd.notnull(row["Latitudine"]) and pd.notnull(row["Longitudine"]):
        popup_html = f'''
        <strong>{row['Titolo']}</strong><br>
        Prezzo base: €{row['Prezzo Base']}<br>
        Superficie: {row['Superficie (mq)']} mq<br>
        Margine netto: €{int(row['Margine Netto Stimato'])}<br>
        <a href="{row['Link']}" target="_blank">Vai all'annuncio</a>
        '''
        color = "green" if row["Margine Netto Stimato"] > 0 else "red"
        folium.Marker(
            location=[row["Latitudine"], row["Longitudine"]],
            popup=popup_html,
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)

folium_static(m)

# Tabella sotto
st.markdown("### Dettaglio Immobili")
st.dataframe(filtro_df.reset_index(drop=True))

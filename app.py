import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Configurazione Pagina Mobile-Friendly
st.set_page_config(page_title="Alpha Shield Dashboard", layout="centered")

st.title("🛡️ Alpha Shield Definitivo 2.0")

# 1. Definizione Asset (basata sulla tua strategia)
assets = {
    "DE000EWG2LD7": {"name": "Euwax Gold II", "weight": 0.20},
    "IE00BKVL7778": {"name": "MSCI Europe Quality", "weight": 0.20},
    "IE00BF4G7076": {"name": "JPM US Research Enhanced", "weight": 0.20},
    "IE00BK5S0507": {"name": "S&P SmallCap 600 Quality", "weight": 0.20},
    "IE00B1FZS798": {"name": "Euro Govt Bond 7-10yr", "weight": 0.20}
}

capitale_iniziale = 110000

# 2. Recupero Dati Real-Time
@st.cache_data(ttl=3600)
def get_data():
    tickers = list(assets.keys())
    data = yf.download(tickers, period="1d")['Close'].iloc[-1]
    return data

try:
    prices = get_data()
    
    # 3. Calcolo Valori
    df_list = []
    for isin, info in assets.items():
        prezzo = prices[isin]
        valore_target = capitale_iniziale * info['weight']
        df_list.append({
            "Asset": info['name'],
            "Peso Target": f"{info['weight']*100}%",
            "Prezzo Attuale": round(prezzo, 2),
            "Valore Stimato (€)": round(valore_target, 2)
        })

    df = pd.DataFrame(df_list)

    # 4. Visualizzazione Mobile
    st.metric(label="Capitale Totale Monitorato", value=f"{capitale_iniziale:,} €")

    st.subheader("Allocazione Portafoglio")
    fig = px.pie(df, values='Valore Stimato (€)', names='Asset', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dettaglio Asset")
    st.dataframe(df, hide_index=True)

    # 5. Sezione Fiscale (Germania)
    with st.expander("ℹ️ Info Fiscali (Germania)"):
        st.write("""
        Essendo residente fiscale in Germania, ricorda che:
        - La **Abgeltungsteuer** è del 25% + Solidaritätszuschlag.
        - Hai una **Sparer-Pauschbetrag** (esenzione) di 1.000€ all'anno.
        - Per gli ETF Equity, si applica la **Teilfreistellung** (esenzione parziale del 30%).
        """)

except Exception as e:
    st.error("Errore nel caricamento dati. Verifica la connessione o i ticker.")

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Alpha Shield Dashboard", layout="centered")
st.title("🛡️ Alpha Shield Definitivo 2.0")

# 1. Asset con Ticker corretti per Yahoo Finance
# Ho sostituito gli ISIN con i simboli di borsa (es. EWG2.DE per l'oro a Francoforte)
assets = {
    "EWG2.DE": {"name": "Euwax Gold II", "weight": 0.20},
    "XDEQ.L": {"name": "MSCI Europe Quality", "weight": 0.20},
    "JREU.L": {"name": "JPM US Research Enhanced", "weight": 0.20},
    "ZPRQ.DE": {"name": "S&P SmallCap 600 Quality", "weight": 0.20},
    "VGE7.DE": {"name": "Euro Govt Bond 7-10yr", "weight": 0.20}
}

capitale_iniziale = 110000

@st.cache_data(ttl=3600)
def get_data():
    tickers = list(assets.keys())
    # Scarichiamo i dati dell'ultimo giorno
    data = yf.download(tickers, period="5d")['Close']
    # Prendiamo l'ultimo prezzo disponibile non nullo
    return data.ffill().iloc[-1]

try:
    prices = get_data()
    
    df_list = []
    for ticker, info in assets.items():
        # Verifichiamo che il prezzo esista
        prezzo = prices[ticker]
        valore_target = capitale_iniziale * info['weight']
        df_list.append({
            "Asset": info['name'],
            "Ticker": ticker,
            "Prezzo (€)": round(prezzo, 2),
            "Valore Target (€)": round(valore_target, 2)
        })

    df = pd.DataFrame(df_list)

    # UI Mobile
    st.metric(label="Capitale Totale", value=f"{capitale_iniziale:,} €")

    fig = px.pie(df, values='Valore Target (€)', names='Asset', hole=0.4)
    fig.update_layout(showlegend=False) # Più pulito su mobile
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dettaglio Asset")
    st.dataframe(df[["Asset", "Prezzo (€)", "Valore Target (€)"]], hide_index=True)

except Exception as e:
    st.error(f"Errore tecnico: {e}")
    st.info("Consiglio: Se l'errore persiste, prova a ricaricare la pagina tra un minuto.")

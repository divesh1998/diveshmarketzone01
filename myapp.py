
import streamlit as st
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# App config
st.set_page_config(page_title="Divesh Market Zone", layout="centered")
st.title("📈 Divesh Market Zone")
st.markdown("**Live BTC Chart + Signal + Image Upload + Auto Support/Resistance**")

# 📤 Image Upload Section
st.header("📤 Upload Chart Image")
uploaded_file = st.file_uploader("Upload your technical setup image", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Chart", use_container_width=True)

    # Save uploaded file (auto-save with timestamp)
    folder = "saved_images"
    os.makedirs(folder, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uploaded_file.name
    with open(os.path.join(folder, filename), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Image saved!")

# 📊 Fetch BTC data using yfinance
st.header("📊 Signal Generator")
btc = yf.download("BTC-USD", period="5d", interval="1h")
btc.dropna(inplace=True)

# Auto support/resistance
support = btc["Low"].min()
resistance = btc["High"].max()
close_price = btc["Close"].iloc[-1]

st.metric("📉 Live BTC Price", f"${close_price:,.2f}")
st.write(f"🟢 **Support Level:** {support:.2f}")
st.write(f"🔴 **Resistance Level:** {resistance:.2f}")

# Wave and Trend Inputs
wave1_high = st.number_input("Wave 1 High", value=resistance * 0.98)
trend = st.selectbox("Market Trend", ["Uptrend", "Downtrend"])
sl = st.number_input("Stop Loss (SL)", value=support)
tp = st.number_input("Take Profit (TP)", value=resistance)

# Signal Logic
signal = ""
if trend == "Uptrend" and close_price > wave1_high:
    signal = "🚀 BUY Signal (Wave 3 Breakout)"
elif trend == "Downtrend" and close_price < wave1_high:
    signal = "📉 SELL Signal (Wave 3 Breakout)"
elif trend == "Uptrend" and close_price > resistance:
    signal = "🔼 BUY Signal (Resistance Break)"
elif trend == "Downtrend" and close_price < support:
    signal = "🔽 SELL Signal (Support Break)"
else:
    signal = "📵 NO TRADING ZONE"

if st.button("Generate Signal"):
    st.subheader("📡 Signal Output:")
    st.success(f"{signal} \n🎯 SL: {sl} | 🏁 TP: {tp}")

# 📈 Candlestick Chart
st.header("📈 Last 5-Day BTC/USDT Chart")

fig = go.Figure(data=[go.Candlestick(
    x=btc.index,
    open=btc["Open"],
    high=btc["High"],
    low=btc["Low"],
    close=btc["Close"]
)])

fig.add_hline(y=support, line=dict(color="green", dash="dot"))
fig.add_hline(y=resistance, line=dict(color="red", dash="dot"))
fig.update_layout(title="Live BTC/USD Candlestick Chart", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

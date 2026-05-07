import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="📊 Stock Market Live Graph", layout="wide")

st.title("📊 Stock Market Live Graph")
st.markdown("---")

# Input
symbol = st.text_input("Enter Stock Symbol (e.g., BHARTIARTL.NS, TCS.NS, RELIANCE.NS)")

col1, col2 = st.columns(2)

if st.button("🚀 Show Live Graph"):
    if not symbol.strip():
        st.warning("⚠️ Please enter a stock symbol!")
    else:
        with st.spinner("Fetching stock data..."):
            try:
                stock = yf.Ticker(symbol.strip().upper())
                data = stock.history(period="1mo")

                if data.empty:
                    st.error("⚠️ No data found. Try another symbol!")
                else:
                    max_price = stock.fast_info["yearHigh"]
                    min_price = stock.fast_info["yearLow"]
                    latest_price = data["Close"].iloc[-1]

                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("📌 Latest Price", f"₹{latest_price:.2f}")
                    col2.metric("📈 52-Week High", f"₹{max_price:.2f}", delta="High")
                    col3.metric("📉 52-Week Low", f"₹{min_price:.2f}", delta="Low")

                    # Alert
                    if latest_price > max_price:
                        st.success(f"📈 {symbol.upper()} has crossed 52-Week High: ₹{latest_price:.2f}")
                    elif latest_price < min_price:
                        st.warning(f"📉 {symbol.upper()} has fallen below 52-Week Low: ₹{latest_price:.2f}")

                    # Plot
                    fig, ax = plt.subplots(figsize=(12, 5))
                    ax.plot(data.index, data["Close"], marker="o", linestyle="-",
                            color="blue", label=f"{symbol.upper()} Price Trend")
                    ax.axhline(y=max_price, color='green', linestyle="--", label="52-Week High")
                    ax.axhline(y=min_price, color='red', linestyle="--", label="52-Week Low")
                    ax.set_xlabel("Date", fontsize=12)
                    ax.set_ylabel("Closing Price (₹)", fontsize=12)
                    ax.set_title(f"Stock Price Trend - {symbol.upper()}", fontsize=14)
                    ax.grid(True)
                    ax.legend()
                    plt.xticks(rotation=45)
                    plt.tight_layout()

                    st.pyplot(fig)

                    st.info("🔄 Auto-refresh ke liye page reload karo ya naya symbol daalo!")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.caption("💡 NSE stocks ke liye .NS lagao — e.g., TCS.NS | BSE ke liye .BO — e.g., TCS.BO")

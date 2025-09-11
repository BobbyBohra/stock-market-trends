import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


# Function to fetch stock data and update graph
def plot_stock_data():
    time.sleep(15)  # हर API कॉल के बीच 15 सेकंड का ब्रेक
    stock_symbol = symbol_entry.get().strip().upper()

    if not stock_symbol:
        messagebox.showwarning("⚠️ Input Error", "Please enter a stock symbol!")
        return

    try:
        # Fetch stock data
        stock = yf.Ticker(stock_symbol)
        data = stock.history(period="1mo")  # Last 1 month data

        if data.empty:
            messagebox.showwarning("⚠️ Data Error", "No stock data found. Try another symbol!")
            return

        # Get 52-week High & Low
        max_price = stock.fast_info["yearHigh"]
        min_price = stock.fast_info["yearLow"]

        dates = data.index
        close_prices = data["Close"]
        latest_price = close_prices.iloc[-1]

        # Check for alerts
        if latest_price > max_price:
            messagebox.showinfo("📈 Price Alert", f"{stock_symbol} has crossed 52-Week High: ₹{latest_price:.2f}")
        elif latest_price < min_price:
            messagebox.showwarning("📉 Price Alert", f"{stock_symbol} has fallen below 52-Week Low: ₹{latest_price:.2f}")

        # Update Labels
        max_price_label.config(text=f"📌 52-Week High: ₹{max_price:.2f}", foreground="green")
        min_price_label.config(text=f"📌 52-Week Low: ₹{min_price:.2f}", foreground="red")

        # Clear previous graph and plot new one
        ax.clear()
        ax.plot(dates, close_prices, marker="o", linestyle="-", color="blue", label=f"{stock_symbol} Price Trend")

        ax.axhline(y=max_price, color='green', linestyle="--", label="52-Week High")
        ax.axhline(y=min_price, color='red', linestyle="--", label="52-Week Low")

        ax.set_xlabel("Date", fontsize=12, color="black")
        ax.set_ylabel("Closing Price (₹)", fontsize=12, color="black")
        ax.set_title(f"Stock Price Trend for {stock_symbol}", fontsize=14, color="black")
        ax.grid(True)
        ax.legend()

        canvas.draw()

        # Auto-refresh every 90 seconds
        root.after(90000, plot_stock_data)  # अब डेटा हर 90 सेकंड बाद अपडेट होगा

    except Exception as e:
        messagebox.showerror("❌ Error", f"Error fetching data: {str(e)}")

# Function to set a clean background
def set_clean_bg(root):
    root.configure(bg="#f0f0f0")

# Creating main window with clean theme
root = tk.Tk()
root.title("📊 Stock Market Live Graph")
root.geometry("850x600")

# Set simple clean background
set_clean_bg(root)

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=10, relief="flat", background="#00ADB5", foreground="white")
style.map("TButton", background=[("active", "#393E46")])

style.configure("TLabel", font=("Arial", 12), background="#f0f0f0", foreground="black")
style.configure("TEntry", font=("Arial", 12), padding=5)

# Label for stock symbol input
symbol_label = ttk.Label(root, text="Enter Stock Symbol (e.g., BHARTIARTL.NS):")
symbol_label.pack(pady=10)

# Entry widget for stock symbol
symbol_entry = ttk.Entry(root, width=30)
symbol_entry.pack(pady=5)

# Labels to show Auto Max & Min Price (52-Week High/Low)
max_price_label = ttk.Label(root, text="📌 52-Week High: Fetching...")
max_price_label.pack(pady=10)

min_price_label = ttk.Label(root, text="📌 52-Week Low: Fetching...")
min_price_label.pack(pady=10)

# Button to get stock data and plot graph
get_data_button = ttk.Button(root, text="Start Live Graph", command=plot_stock_data)
get_data_button.pack(pady=15)

# Matplotlib Figure and Axes (Clean theme)
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_facecolor("#f0f0f0")
fig.patch.set_facecolor("#f0f0f0")

# Embed Matplotlib Figure into Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=15)

# Run the GUI
root.mainloop()

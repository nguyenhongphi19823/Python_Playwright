import ccxt
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Binance API
binance = ccxt.binance()

# Define the token pairs to fetch
token_pairs = [
    "BTC/USDT", "ETH/USDT"
]

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # Change if using another service
SMTP_PORT = 587
EMAIL_SENDER = "nguyenhongphi19823@gmail.com"
EMAIL_PASSWORD = "xtgs xbsa xjhh mgcp"  # Use App Password for Gmail
EMAIL_RECEIVER = "nguyenhongphi19823@gmail.com"


def send_email(subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


# Bollinger Bands calculation function
def calculate_bollinger_bands(data, period=20, std_dev=2):
    if len(data) < period:
        return data  # Return as is if not enough data points
    data["SMA"] = data["close"].rolling(window=period).mean()
    data["STD"] = data["close"].rolling(window=period).std()
    data["Upper_Band"] = data["SMA"] + (data["STD"] * std_dev)
    data["Lower_Band"] = data["SMA"] - (data["STD"] * std_dev)
    return data


# Function to fetch historical OHLCV data
def fetch_ohlcv(symbol, timeframe="5m", lookback_hours=24):
    since = binance.milliseconds() - lookback_hours * 60 * 60 * 1000
    try:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=since)
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None


# Find tokens touching the upper Bollinger Band
def find_potential_downtrends(timeframe="5m"):
    results = []
    for pair in token_pairs:
        df = fetch_ohlcv(pair, timeframe)
        if df is None or len(df) < 20:  # Ensure enough data
            continue

        df = calculate_bollinger_bands(df)

        # Check if the latest close price touches the upper Bollinger Band
        last_close = df.iloc[-1]["close"]
        last_upper_band = df.iloc[-1]["Upper_Band"]

        if last_close >= last_upper_band:
            results.append(pair)

        # Add a small delay to avoid hitting rate limits
        time.sleep(0.5)

    return results


# Run the check
tokens_to_watch = find_potential_downtrends()

if tokens_to_watch:
    message = f"The following tokens are touching the upper Bollinger Band:\n\n" + "\n".join(tokens_to_watch)
    print("Tokens likely to decrease:", tokens_to_watch)
    send_email("Crypto Could be Dump: Potential Opportunities for Bollinger Band_5m", message)
else:
    print("No tokens meeting the condition.")

#    Test email function
#   send_email("Test Email", "This is a test email to verify SMTP settings.")
#   print("Test email sent successfully!")


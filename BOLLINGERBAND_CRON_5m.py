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
    "BTC/USDT", "XRP/USDT", "WLD/USDT", "OP/USDT", "KDA/USDT", "ETH/USDT",
    "SOL/USDT", "BNB/USDT", "TON/USDT", "SUI/USDT", "XLM/USDT", "MINA/USDT",
    "OM/USDT", "ATOM/USDT", "FTM/USDT", "ARB/USDT", "METIS/USDT", "MANTA/USDT",
    "POL/USDT", "SKL/USDT", "IMX/USDT", "UNI/USDT", "AAVE/USDT",
    "LINK/USDT", "SUSHI/USDT", "COMP/USDT", "MKR/USDT", "YFI/USDT", "CAKE/USDT",
    "CRV/USDT", "SNX/USDT", "BAL/USDT", "LDO/USDT", "ADA/USDT", "DOT/USDT",
    "XTZ/USDT", "VET/USDT", "AVAX/USDT", "POLYX/USDT", "HIFI/USDT", "ENA/USDT",
    "TRX/USDT", "TAO/USDT", "NEAR/USDT", "ETC/USDT", "APT/USDT", "S/USDT",
    "INJ/USDT", "ICP/USDT", "STX/USDT", "THETA/USDT", "SEI/USDT", "MOVE/USDT",
    "NEO/USDT", "BERA/USDT", "IOTA/USDT", "QTUM/USDT", "KAIA/USDT", "FLOW/USDT",
    "CFX/USDT", "KAVA/USDT", "AXL/USDT", "ZK/USDT", "ASTR/USDT", "KSM/USDT",
    "CKB/USDT", "ZIL/USDT", "DYM/USDT", "DYM/USDT", "HOT/USDT", "ELF/USDT",
    "OSMO/USDT", "DCR/USDT", "ENJ/USDT", "SKL/USDT", "ONE/USDT", "VANA/USDT",
    "ONT/USDT", "IOTX/USDT", "SXP/USDT", "LSK/USDT", "HIVE/USDT", "AEVO/USDT",
    "FLUX/USDT", "CHR/USDT", "ICX/USDT", "GLMR/USDT", "CELR/USDT", "WAXP/USDT",
    "SCR/USDT", "CTSI/USDT", "OMNI/USDT", "ARK/USDT", "SCRT/USDT", "MOVR/USDT",
    "BB/USDT", "NTRN/USDT", "PHB/USDT", "CTXC/USDT", "VIC/USDT",
    "SLF/USDT", "WAN/USDT", "NULS/USDT", "COMBO/USDT", "ACH/USDT", "COTI/USDT",
    "XNO/USDT", "PUNDIX/USDT", "UTK/USDT", "DUSK/USDT", "TRU/USDT",
    "PROS/USDT", "LTO/USDT", "FET/USDT", "GRT/USDT", "LPT/USDT", "IO/USDT",
    "ACT/USDT", "AIXBT/USDT", "PHA/USDT", "POND/USDT", "CGPT/USDT", "IQ/USDT",
    "RLC/USDT", "COOKIE/USDT", "NMR/USDT", "AI/USDT", "NFP/USDT", "MDT/USDT",
    "ENS/USDT", "RENDER/USDT", "TIA/USDT", "QNT/USDT", "JASMY/USDT", "PYTH/USDT",
    "ZRO/USDT", "W/USDT", "AXL/USDT", "EIGEN/USDT", "TWT/USDT", "KAITO/USDT",
    "SFP/USDT", "GLM/USDT", "ID/USDT", "BAT/USDT", "ARKM/USDT", "MASK/USDT",
    "T/USDT", "ALT/USDT", "G/USDT", "BICO/USDT", "LAYER/USDT", "BAND/USDT",
    "SSV/USDT", "FIDA/USDT", "CVC/USDT", "TRB/USDT", "OXT/USDT", "RAD/USDT",
    "API3/USDT", "DIA/USDT", "ARPA/USDT", "CTK/USDT", "CYBER/USDT", "ATA/USDT",
    "MAV/USDT", "NKN/USDT", "HOOK/USDT", "GTC/USDT", "HEI/USDT", "CLV/USDT",
    "DATA/USDT", "ADX/USDT", "FIO/USDT", "RAY/USDT", "JUP/USDT", "JTO/USDT"

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


# Find tokens touching the lower Bollinger Band
def find_potential_uptrends(timeframe="5m"):
    results = []
    for pair in token_pairs:
        df = fetch_ohlcv(pair, timeframe)
        if df is None or len(df) < 20:  # Ensure enough data
            continue

        df = calculate_bollinger_bands(df)

        # Check if the latest close price touches the lower Bollinger Band
        last_close = df.iloc[-1]["close"]
        last_lower_band = df.iloc[-1]["Lower_Band"]

        if last_close <= last_lower_band:
            results.append(pair)

        # Add a small delay to avoid hitting rate limits
        time.sleep(0.5)

    return results


# Run the check
tokens_to_watch = find_potential_uptrends()

if tokens_to_watch:
    message = f"The following tokens are touching the lower Bollinger Band:\n\n" + "\n".join(tokens_to_watch)
    print("Tokens likely to increase:", tokens_to_watch)
    send_email("Crypto Trading Alert: Potential Opportunities for Bollinger Band_5m", message)
else:
    print("No tokens meeting the condition.")

#    Test email function
#   send_email("Test Email", "This is a test email to verify SMTP settings.")
#   print("Test email sent successfully!")


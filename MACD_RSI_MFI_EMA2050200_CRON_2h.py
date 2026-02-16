import ccxt
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta

# Initialize Binance API
exchange = ccxt.binance()

# Full token pairs list
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

# Fetch latest candles
def fetch_data(symbol, timeframe='2h'):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=500)
        ohlcv_df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        ohlcv_df['timestamp'] = pd.to_datetime(ohlcv_df['timestamp'], unit='ms', utc=True)
        return ohlcv_df
    except ccxt.BaseError as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

# Calculate MACD
def calculate_macd(df, short=12, long=26, signal=9):
    df['ema_short'] = df['close'].ewm(span=short, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long, adjust=False).mean()
    df['macd'] = df['ema_short'] - df['ema_long']
    df['signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
    return df

# Calculate RSI
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).ewm(alpha=1/period, adjust=False).mean()
    avg_loss = pd.Series(loss).ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

# Calculate MFI
def calculate_mfi(df, period=14):
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    money_flow = typical_price * df['volume']
    positive_flow = np.where(typical_price > typical_price.shift(1), money_flow, 0)
    negative_flow = np.where(typical_price < typical_price.shift(1), money_flow, 0)
    sum_positive_flow = pd.Series(positive_flow).rolling(window=period, min_periods=1).sum()
    sum_negative_flow = pd.Series(negative_flow).rolling(window=period, min_periods=1).sum()
    mfi = 100 * (sum_positive_flow / (sum_positive_flow + sum_negative_flow + 1e-10))
    df['mfi'] = mfi
    return df

# Calculate Moving Averages (EMA)
def calculate_ema(df, period):
    df[f'ema_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    return df

# Calculate MAVOL
def calculate_mavol(df, period=14):
    df['mavol'] = df['volume'].rolling(window=period, min_periods=1).mean()
    return df

# Check conditions
def check_conditions(df):
    if df.empty or len(df) < 21:
        return False

    latest = df.iloc[-1]
    previous = df.iloc[-2]
    ten_back = df.iloc[-11] if len(df) > 10 else latest
    twenty_back = df.iloc[-21] if len(df) > 20 else latest
    thirty_back = df.iloc[-31] if len(df) > 30 else latest
    # Debugging
    print(f"\n🔍 Checking conditions for {latest['timestamp']} UTC:")
    print(f"MACD: {latest['macd']:.4f}, Signal: {latest['signal']:.4f}")
    print(f"RSI: {latest['rsi']:.4f}, MFI: {latest['mfi']:.4f}")
    print(f"Volume: {latest['volume']:.2f}, MAVOL: {latest['mavol']:.2f}")
    print(f"EMA 7: {latest['ema_7']:.4f}, EMA 50: {latest['ema_50']:.4f}, EMA 200: {latest['ema_200']:.4f}")

    conditions = [
        # Condition 1
        latest['macd'] > latest['signal'] and
        40 < latest['rsi'] < 80 and
        40 < latest['mfi'] < 80 and
        #latest['volume'] > latest['mavol'] and
        #previous['volume'] > previous['mavol'] and
        latest['ema_50'] > latest['ema_200'] and
        previous['ema_50'] > previous['ema_200'] and
        thirty_back['ema_50'] < thirty_back['ema_200'],
        #latest['ema_7'] > latest['ema_50'] > latest['ema_200'] and
        #twenty_back['ema_7'] < twenty_back['ema_50'] < twenty_back['ema_200'],

        # Condition 2
        latest['macd'] > latest['signal'] and
        previous['rsi'] < latest['rsi'] < 35 and
        previous['mfi'] < latest['mfi'] < 35 and
        #latest['volume'] > latest['mavol'] and
        #previous['volume'] > previous['mavol'] and
        latest['ema_50'] > latest['ema_200'] and
        previous['ema_50'] > previous['ema_200'] and
        thirty_back['ema_50'] < thirty_back['ema_200'],
        #latest['ema_7'] > latest['ema_50'] > latest['ema_200'] and
        #twenty_back['ema_7'] < twenty_back['ema_50'] < twenty_back['ema_200'],
    ]

    return any(conditions)

# Find opportunities
def find_opportunities(symbols):
    opportunities = []
    for symbol in symbols:
        print(f"\nFetching data for {symbol}...")
        df = fetch_data(symbol)
        if df.empty:
            print(f"No data found for {symbol}. Skipping...")
            continue
        df = calculate_macd(df)
        df = calculate_rsi(df)
        df = calculate_mfi(df)
        df = calculate_mavol(df)
        for period in [7, 50, 200]:
            df = calculate_ema(df, period)

        if check_conditions(df):
            opportunities.append(symbol)

    return opportunities

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "nguyenhongphi19823@gmail.com"
EMAIL_PASSWORD = "xtgs xbsa xjhh mgcp"
EMAIL_RECEIVER = "nguyenhongphi19823@gmail.com"

# Send email notification
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

        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Find potential opportunities
opportunities = find_opportunities(token_pairs)

# Print results and send email
if opportunities:
    print("\n🔥 Cryptos with potential price increase:\n")
    for opportunity in opportunities:
        print(f"✅ {opportunity}")

    subject = "🚀 Crypto Trading Alert: Potential Opportunities for MACD_RSI_MFI_EMA2050200_2h"
    message = "The following cryptocurrencies meet the trading conditions:\n\n" + "\n".join(opportunities)
    send_email(subject, message)
else:
    print("\n❌ No trading opportunities found.")

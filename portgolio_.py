import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import mplfinance as mpf

# Google Sheets API認証設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Google Sheetsからデータを取得
sheet = client.open("シート名").worksheet("Sheet2")  # シート名を指定
data = sheet.get_all_records()

# DataFrameに変換
df = pd.DataFrame(data)

# 日付をDatetimeに変換
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# 株価データを数値型に変換
df['stockPrice'] = pd.to_numeric(df['stockPrice'], errors='coerce')

# ロウソク足チャート用のフォーマットに変換
ohlc = df.groupby(pd.Grouper(freq='D')).agg({
    'stockPrice': ['first', 'max', 'min', 'last']
})
ohlc.columns = ['Open', 'High', 'Low', 'Close']
ohlc.dropna(inplace=True)

# ロウソク足チャートを作成
mpf.plot(
    ohlc,
    type='candle',
    style='charles',
    title='株価変動チャート',
    ylabel='Price',
    ylabel_lower='Volume',
    datetime_format='%Y-%m-%d',
    savefig='candlestick_chart.png'
)

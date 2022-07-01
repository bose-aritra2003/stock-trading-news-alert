import os
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ.get("STOCK_API_KEY")
}
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_params = {
    "q": COMPANY_NAME,
    "apiKey": os.environ.get("NEWS_API_KEY")
}
stock_data = requests.get(url=STOCK_ENDPOINT, params=stock_params).json()
yesterday_stock = float(stock_data["Time Series (Daily)"]["2022-05-12"]["4. close"])
day_before_stock = float(stock_data["Time Series (Daily)"]["2022-05-11"]["4. close"])
difference = yesterday_stock - day_before_stock
emoji = None
if difference < 0:
    emoji = "🔻"
else:
    emoji = "🔺"
percentage_diff = round(abs(difference) / yesterday_stock * 100)
news_data = requests.get(url=NEWS_ENDPOINT, params=news_params).json()
first_three_news = news_data["articles"][:3]

account_sid = "ACaf886c4468a4adbdbf01fbde77866825"
auth_token = os.environ.get("TWILO_AUTH_TOKEN")
twilio_number = "+19853228901"
client = Client(account_sid, auth_token)
three_articles = [{"headline": item["title"], "description": item["description"]} for item in first_three_news]
if percentage_diff >= 0:
    for news in three_articles:
        client.messages.create(
            body=f"{STOCK_NAME}: {emoji} {percentage_diff}%\n"
                 f"Headline: {news['headline']}\n"
                 f"Brief: {news['description']}\n",
            from_=twilio_number,
            to='+917003232611'
        )

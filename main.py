import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"
account_sid = "Your Twilio acc_sid"
auth_token = "Your Twilio acc token"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API = "your_av_api_token"
NEWS_API = "your_news_api_token"
stocks_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API,
}
stocks_response = requests.get(url=STOCK_ENDPOINT, params=stocks_params)
stocks_response.raise_for_status()
stocks_response_data = stocks_response.json()["Time Series (Daily)"]

stocks_data = [value for (key, value) in stocks_response_data.items()]
y_price = float(stocks_data[0]["4. close"])
dby_price = float(stocks_data[1]["4. close"])
positive_diff = y_price - dby_price
up_or_down = None
if positive_diff > 0:
    up_or_down = "🔼"
else:
    up_or_down = "🔽"

percentage = float("%.2f" % (100 * (positive_diff / y_price)))
print(percentage)


if abs(percentage) > 1:
    news_param = {
        "qInTitle": COMPANY_NAME,
        "language": "en",
        "apiKey": NEWS_API
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_param)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    three_news = news_data[:3]

    msg_list = [f"{COMPANY_NAME}: {up_or_down}{positive_diff}%\nHeadline:{article['title']}. \nBrief: {article['description']}" for article in three_news]
    print(msg_list)

    client = Client(account_sid, auth_token)
    for msg in msg_list:
        message = client.messages \
            .create(
                body=msg,
                from_='your_twilio_number',
                to="your_mobile_number"
            )



from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

# get today's date in year-month-day 00:00:00 format
today = datetime.utcnow().date()
time = datetime.min.time()
today_date_time = datetime.combine(today, time)

# get date five years ago
five_years_ago = today_date_time - relativedelta(years=5)

# convert datetime into Unix timestamp
unix_today = int(today_date_time.timestamp())
unix_five_years_ago = int(five_years_ago.timestamp())

# get url of web page
url = "https://finance.yahoo.com/quote/"
markets = {'DJI': '%5EDJI', 'S&P500': '%5EGSPC', 'NASDAQ Composite': '%5EIXIC'}
url_list = []

for market in list(markets.keys()):
    full_url = url + markets[market] + '/history?period1=' + str(unix_five_years_ago) + '&period2=' + str(
        unix_today) + '&interval=1d&filter=history&frequency=1d '
    url_list.append(full_url)

# include try/except
response_url = requests.get(url_list[0])

# web scraping
html_soup = BeautifulSoup(response_url.text, 'html.parser')
day_container = html_soup.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')

all_price = []  # 2D array for each entry
for day in day_container:
    soup_tag = [str(val.get_text()) for val in day.find_all('span')]
    individual_price = [price.replace(",", "") for price in soup_tag]  # replace comma with space to convert into float
    price_entry = []  # initialize new array to put converted value
    for num in range(len(individual_price)):
        # print(type(individual_price[num]))
        if num != 0:
            price = individual_price[num]
            float_price = float(price)
            price_entry.append(float_price)
        else:
            date = datetime.strptime(individual_price[num], "%b %d %Y").date()
            price_entry.append(date)
    all_price.append(price_entry)

# convert array into dataframe
dji = pd.DataFrame(all_price, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
dji = dji.set_index('Date')
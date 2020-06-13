from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

# get today's date in year-month-day 00:00:00 format
today = datetime.utcnow().date()
time = datetime.min.time()
today_date_time = datetime.combine(today, time)

# get date five years ago
five_years_ago = today_date_time - relativedelta(years=5)

# convert datetime into Unix timestamp
unix_today = int(today_date_time.timestamp())
unix_five_years_ago = int(five_years_ago.timestamp())

# print(today_date_time)
# print(five_years_ago)
# print(unix_today)
# print(unix_five_years_ago)

# get url of web page
url = "https://finance.yahoo.com/quote/"
market = {'DJI': '%5EDJI'}

full_url = url + market['DJI'] + '/history?period1=' + str(unix_five_years_ago) + '&period2=' + str(
    unix_today) + '&interval=1d&filter=history&frequency=1d '

# print(full_url)

response_url = requests.get(url)

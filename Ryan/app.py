import requests
import time
from bs4 import BeautifulSoup


# Select the resource to download
resource_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

# Request to download the file from the Internet
response = requests.get(resource_url, time.sleep(10)).text

if "403 Forbidden" in response:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    request = requests.get(resource_url, headers = headers)
    time.sleep(10)
    html_data = request.text

soup = BeautifulSoup(response, 'html.parser')

soup
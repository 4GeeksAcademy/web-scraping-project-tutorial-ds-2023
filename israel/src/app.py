import time
import pandas as pd
import requests
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup


resource_url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

response = requests.get(resource_url, time.sleep(10)).text

if "403 Forbidden" in response:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    request = requests.get(resource_url, headers = headers)
    time.sleep(10)
    response = request.text

soup = BeautifulSoup(response, features= "html.parser")

tables = soup.find_all("table")

for index, table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index
        break

# Tried this method first but couldn't figure out lxml errors 
#tesla_revenue = pd.read_html(str(tables)[table_index])
#tesla_revenue.columns = ["Date", "Revenue"]
#tesla_revenue["Revenue"]= tesla_revenue["Revenue"].str.replace('[$,]', '', regex=True).astype(float)

tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({
            "Date": Date,
            "Revenue": Revenue
        }, index = [0])], ignore_index = True)


tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]

con = sqlite3.connect("Tesla_Revenue_DB")
cursor = con.cursor()
cursor.execute("""CREATE TABLE revenue (Date, Revenue)""")
tesla_tuples = list(tesla_revenue.to_records(index = False))
cursor.executemany("INSERT INTO revenue VALUES (?,?)", tesla_tuples)
con.commit()

fig, axis = plt.subplots(figsize = (10, 5))
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype('int')
tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
tesla_revenue_yearly = tesla_revenue.groupby(tesla_revenue["Date"].dt.year).sum().reset_index()
tesla_revenue_monthly = tesla_revenue.groupby(tesla_revenue["Date"].dt.month).sum().reset_index()

sns.barplot(data = tesla_revenue_yearly[tesla_revenue_yearly["Date"] < 2023], x = "Date", y = "Revenue")
sns.barplot(data = tesla_revenue_monthly, x = "Date", y = "Revenue")
sns.lineplot(data = tesla_revenue, x = "Date", y = "Revenue")

plt.tight_layout()

plt.show()
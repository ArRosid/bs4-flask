import requests
from bs4 import BeautifulSoup
import json
import csv

url = "https://www.free-proxy-list.net/"

res = requests.get(url)

# print(res.status_code)
# print(res.headers)
# print(res.text)


results = []

soup = BeautifulSoup(res.text, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')

headers = [header.text for header in rows[0]]

results.append(headers)

for row in rows:
    if len(row.find_all('td')) > 0:
        data = [td.text for td in row]
        results.append(data)

print(json.dumps(results, indent=3))

with open('proxy_list.csv', 'w') as output:
    writer = csv.writer(output)
    writer.writerows(results)
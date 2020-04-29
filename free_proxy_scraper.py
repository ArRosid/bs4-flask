import requests
from bs4 import BeautifulSoup
import json
import csv


class ProxyScraper:
    results = []

    def fetch(self, url):
        """Fetch data from url"""
        return requests.get(url)

    def parse(self, html):
        """Parse the result of fetch"""
        soup = BeautifulSoup(html, 'html.parser')

        table = soup.find('table')
        rows = table.find_all('tr')

        headers = [header.text for header in rows[0]]

        self.results.append(headers)

        for row in rows:
            if len(row.find_all('td')) > 0:
                data = [td.text for td in row]
                self.results.append(data)

    def to_csv(self):
        """Export parsed data to csv"""
        with open('proxy_list.csv', 'w') as output:
            writer = csv.writer(output)
            writer.writerows(self.results)

    def run(self):
        """Run the scraper"""
        res = self.fetch('https://www.free-proxy-list.net/')
        self.parse(res.text)
        self.to_csv()


if __name__ == '__main__':
    scraper = ProxyScraper()
    scraper.run()

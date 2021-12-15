from bs4 import BeautifulSoup
from Scraper import Scraper
from matplotlib import pyplot as plt


class Corona_scraper(Scraper): # This class is an example of how Scraper can be extended for specific cases
    def __init__(self):
        self.url = "https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/"
        self.depth = 0
        super().__init__()
        self.data = []
    
    def scrape_corona_data(self):
        res = self.fetch_html(self.url)
        if res == None:
            return
        content = res.text
        soup = BeautifulSoup(content, features='lxml')
        table = soup.find('table', id='table3')
        rows = table.find_all('tr')
        for i in range(1, len(rows)): # Skips the first row
            entries = rows[i].find_all('td')
            country = entries[0].getText()
            cases = int(entries[1].getText().replace(',', ''))
            deaths = int(entries[2].getText().replace(',',''))
            self.data.append((country, cases, deaths))
    
    def visualize(self):
        # Only plots the ten countries with the most cases
        data = self.data
        labels = [data[i][0] for i in range(0, 9)]
        values = [data[i][1] for i in range(0, 9)]
        plt.bar(labels, values)
        plt.savefig('fig.png', dpi=199)


if __name__=='__main__':
    s = Corona_scraper()
    s.scrape_corona_data()
    s.visualize()
        

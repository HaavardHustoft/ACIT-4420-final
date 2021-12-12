from bs4 import BeautifulSoup
from Scraper import Scraper
from matplotlib import pyplot as plt


class Corona_scraper(Scraper): # This class is an example of how Scraper can be extended for specific cases
    def __init__(self, url="https://www.worldometers.info/coronavirus/countries-where-coronavirus-has-spread/", depth=0):
        super().__init__(url, depth)
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
            cases = entries[1].getText()
            deaths = entries[2].getText()
            self.data.append((country, cases, deaths))
    
    def visualize(self):
        data = self.data


            
        


if __name__=='__main__':
    s = Corona_scraper()
    s.scrape_corona_data()
        

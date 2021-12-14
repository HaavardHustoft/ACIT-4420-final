import unittest
from Scraper import Scraper
from Corona_scraper import Corona_scraper

class Main(unittest.TestCase):
    def test_corona_scraper(self):
        number_of_entries = 223 # We know that the table on the website has 222 entries, 222 countries and 1 header
        c = Corona_scraper()
        c.scrape_corona_data()
        self.assertEqual(number_of_entries, len(c.data))
    


if __name__=='__main__':
    unittest.main()
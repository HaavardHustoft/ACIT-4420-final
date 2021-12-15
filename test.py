import unittest
from Scraper import Scraper
from Corona_scraper import Corona_scraper

class Main(unittest.TestCase):
    def test_corona_scraper(self):
        number_of_entries = 223 # We know that the table on the website has 222 entries, 222 countries and 1 header
        c = Corona_scraper()
        c.scrape_corona_data()
        self.assertEqual(number_of_entries, len(c.data))
    
    def test_find_elements_by_tag(self):
        s = Scraper()
        res = s.find_elements_by_tag(
            'https://crawler-test.com/canonical_tags/relative_canonical_tag', 'a')
        self.assertEqual(len(res), 1)
    
    def test_find_elements_by_id(self):
        s = Scraper()
        res = s.find_element_by_id(
            'https://crawler-test.com/canonical_tags/relative_canonical_tag', 'logo')
        self.assertTrue(res != None)
    
    def test_exists(self):
        s = Scraper()
        res = s.exists(
            'https://www.uio.no', r'(Forsiden - Universitetet i Oslo)')
        self.assertTrue(res)
    
    def test_find_tag(self):
        s = Scraper()
        res = s.find_tag('https://www.uio.no', 'nav')
        self.assertTrue(res != None)
    
    


if __name__=='__main__':
    unittest.main()
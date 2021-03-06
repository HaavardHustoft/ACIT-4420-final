import unittest

from bs4 import BeautifulSoup, FeatureNotFound
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
    
    def test_find_custom(self):
        s = Scraper()
        content = s.fetch_html(
            'https://crawler-test.com/content/custom_text').text
        res = s.find_custom(content, r'Custom\s[a-z]{4}')
        self.assertEqual(res, ['Custom text', 'Custom text', 'Custom text'])
    
    def test_find_comments(self):
        s = Scraper()
        content = s.fetch_html('https://crawler-test.com/content/custom_text').text
        res = s.find_comments(content)
        self.assertEqual(res, [' Google Tag Manager ', ' End Google Tag Manager '])
    
    def test_find_phone_numbers(self):
        s = Scraper()
        content = s.fetch_html('https://uio.no').text
        res = s.find_phone_numbers(content)
        self.assertEqual(res, ['22 85 66 66'])
    
    def test_find_emails(self):
        s = Scraper()
        content = s.fetch_html(
            'https://www.mn.uio.no/').text
        res = s.find_emails(content)
        self.assertEqual(res, ['postmottak@mn.uio.no',
                         'postmottak@mn.uio.no', 'nettredaktor@mn.uio.no'])
    
    def test_find_urls(self):
        s = Scraper()
        soup = BeautifulSoup(s.fetch_html(
            'https://crawler-test.com/links/page_with_external_links').text, features='lxml')
        res = s.find_urls(soup)
        self.assertEqual(len(res), 5)


if __name__=='__main__':
    unittest.main()
from Scraper import Scraper
from Corona_scraper import Corona_scraper
import time

if __name__=='__main__':
    start = time.time()
    s = Scraper()
    s.start_scraping('https://www.uio.no', 1, [r'\b[0-9]{11}', r'Rektor'])
    end = time.time()
    print(end-start)
    stats = s.get_stats()
    print(stats)

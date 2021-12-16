from Scraper import Scraper
import time

if __name__=='__main__':
    start_url = input("Please specify a url to start the crawl:\n")
    depth = int(input("Scraping depth?\n"))
    start = time.time()
    s = Scraper()
    s.start_scraping(start_url, depth, [r'\b[0-9]{11}', r'Rektor'])
    end = time.time()
    print("Time spent scraping: {}s\n".format(round(end-start, 2)))
    averages = s.get_stats()
    print("Average urls found: {}, Average emails found: {}, Average phone numbers found: {}\n".format(*averages))
    save = (input("Save results to file? (y/n):\n") == "y")
    if save:
        print("Saving results to output.txt ...\n")
        s.save_result()


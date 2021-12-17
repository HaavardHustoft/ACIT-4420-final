from Scraper import Scraper
import time
import matplotlib.pyplot as plt


def test_time_demand(url):
    times = []
    max_depth = 4
    for i in range (5):
        l = []
        for depth in range(max_depth):
            start = time.time()
            s = Scraper()
            s.start_scraping(url, depth)
            end = time.time()
            t = end - start
            l.append(t)
        times.append(l)
    averages = [0 for i in range(max_depth)]
    for l in times:
        for i in range(max_depth):
            averages[i] += l[i]
    for i in range(max_depth):
        averages[i] = round(averages[i] / len(times), 2)
    
    plt.plot(averages)
    plt.xticks([i for i in range(0, max_depth)])
    plt.xlabel('Depth')
    plt.ylabel('Seconds')
    plt.title('Average execution time when starting from {}'.format(url))
    plt.savefig('times.png')

if __name__=='__main__':
    test_time_demand('https://uio.no')
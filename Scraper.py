import requests
import time
import re
import lxml.html
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url: str, depth: int, custom_searches=None, filename='output.txt', optional_args=None):
        self.url = url # Url to start scraping at
        self.depth = depth # Depth of urls to scrape
        self.custom_searches = custom_searches
        self.common_words = []
        self.urls = []
        self.phone_numbers = []
        self.emails = []
        self.comments = []
        self.output = open(filename, 'w')
        self.start_scraping()
        print(*self.emails)
    
    def start_scraping(self):
        self.scrape(self.url, self.depth)
    
    def write_to_file(self, input):
        for item in input:
            self.output.write("     {}\n".format(item))


    def scrape(self, url: str, current_depth: int): # Start the scraping process
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except requests.exceptions.ConnectionError as e:
            print(e)
            return

        content = res.text
        soup = BeautifulSoup(content, features='lxml')
        urls = self.find_urls(soup)

        # All lists are formatted as a tuple (url, list_of_results)
        self.urls.append((url, urls))
        self.phone_numbers.append((url, self.find_phone_numbers(content)))
        self.emails.append((url, self.find_emails(content)))
        self.comments.append((url, self.find_comments(content)))
        self.common_words.append((url, self.find_common_words(soup)))
        
        """ self.output.write("{}\n".format(url))

        if self.custom_searches != None:
            res = self.custom_search(content)
            for i in res:
                self.output.write("Result from custom search \"{}\"\n:".format(i[0]))
                self.write_to_file(i[1])

        if len(urls) > 0:
            self.output.write("Urls found on this site:\n")
            self.write_to_file(urls)
        
        if len(emails) > 0:
            self.output.write("Emails found on this site:\n")
            self.write_to_file(emails)
        
        if len(phone_numbers) > 0:
            self.output.write("Phone numbers found on this site:\n")
            self.write_to_file(phone_numbers)
        
        if len(comments) > 0:
            self.output.write("Comments found on this site:\n")
            self.write_to_file(comments)
        self.output.write("---------------------------------------------\n") """

        if current_depth == 0:
            return
        else:
            for u in urls:
                self.scrape(u, current_depth - 1) # Recursively scrape urls when depth > 0
    
    def custom_search(self, content: str):
        result = []
        for r in self.custom_searches:
            regex = re.compile(r)
            result.append((r, regex.findall(content)))
        return result

    def find_urls(self, soup: BeautifulSoup):
        links = [i.get('href') for i in soup.find_all(
            'a', href=re.compile(r'((http|https)[^\"]*)'))]
        return links
    
    def find_emails(self, content: str):
        # Only finds emails ending with com,org,no,edu or live
        # Regex also works great here as the emails can be found in many different tags, so BeautifulSoup is not necesarry here
        regex = re.compile(
            r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.(com|no|edu|org|live))')
        emails = regex.findall(content)
        if (len(emails) > 0):
            for i in range(0, len(emails)):
                emails[i] = emails[i][0]
        return emails

    def find_phone_numbers(self, content: str):
        # I am not using BeautifulSoup for this one because it is simpler to just use a regular expression
        regex = re.compile(
            r'(((\+4[0-9])\s\d{2}\s\d{2}\s\d{2}\s\d{2})|(\d{2}\s\d{2}\s\d{2}\s\d{2})|((?=href=)\"tel:\d{8}\"))')
        phone_numbers = [match[0] for match in regex.findall(content)] # We only want the first capture group in each match
        return phone_numbers
    
    def find_comments(self, content: str):
        regex = re.compile(r'(<!--([a-zA-z0-9\s.-_,]+)-->)')
        comments = [match[1] for match in regex.findall(content)]
        return comments
    
    def find_common_words(self, soup: BeautifulSoup):
        regex = re.compile(r'[a-zA-Z0-9.,\-!?]+') # only interested in actual words, not symbols
        text_elements = [list(filter(lambda x: x if regex.match(x)
         else "",i.getText(strip=True).split())) for i in soup.find_all(['p','strong','br', 'span', 'em'])]
        
        unique_words = []
        for i in range(len(text_elements)):
            for word in text_elements[i]:
                if not (word in unique_words):
                    unique_words.append(word)
        
        highest = 0
        most_common_word = None
        for word in unique_words:
            counter = 0
            for element in text_elements:
                for w in element:
                    if w == word:
                        counter += 1
            if counter > highest:
                highest = counter
                most_common_word = word
        return most_common_word


if __name__ == '__main__':
    start = time.time()
    s = Scraper(
        'https://www.vg.no', 0)
    end = time.time()
    print(end-start)

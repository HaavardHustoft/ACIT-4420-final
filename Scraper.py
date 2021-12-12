import requests
import time
import re
import lxml.html
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url: str, depth: int, custom_searches=None, optional_args=None):
        self.url = url # Url to start scraping at
        self.depth = depth # Depth of urls to scrape
        self.custom_searches = custom_searches
        self.common_words = []
        self.urls = []
        self.phone_numbers = []
        self.emails = []
        self.comments = []
        self.visited_urls = []
        if optional_args:
            for arg in optional_args:
                if arg == 'save':
                    self.save_result()
    
    def start_scraping(self):
        self.scrape(self.url, self.depth)
    
    def write_to_file(self, input):
        for item in input:
            self.output.write("     {}\n".format(item))
    
    def fetch_html(self, url: str):
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            return res
        except requests.exceptions.ConnectionError as e:
            print(e)
            return None

    
    def save_result(self, filename='output.txt'): # save result of crawl to a text file
        with open(filename, 'w') as output:
            output.write("{}\n".format(self.url))
            """ if self.custom_searches != None:
                res = self.custom_search(content)
                for i in res:
                    self.output.write(
                        "Result from custom search \"{}\"\n:".format(i[0]))
                    self.write_to_file(i[1]) """

            if len(self.urls) > 0:
                output.write("Urls found:\n")
                for item in self.urls:
                    output.write("{}:\n".format(item[0]))
                    for url in item[1]:
                        output.write("  {}\n".format(url))

            for item in self.emails:
                output.write("{} emails: {}\n".format(item[0], item[1]))
            
            for item in self.phone_numbers:
                output.write("{} phone numbers: {}\n".format(item[0], item[1]))
            
            for item in self.comments:
                output.write("{} comments: {}\n".format(item[0], item[1]))


    def scrape(self, url: str, current_depth: int): # Start the scraping process
        if url in self.visited_urls:
            return
        
        res = self.fetch_html(url)

        if res == None:
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
        
        self.visited_urls.append(url) # Marks this ulr as already scraped

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
    
    def custom_search_soup(self, soup: BeautifulSoup, search_param: str):
        pass


    def find_urls(self, soup: BeautifulSoup):
        links = [i.get('href') for i in soup.find_all(
            'a', href=re.compile(r'((http|https)[^\"]+)'))]
        return links
    
    def find_emails(self, content: str):
        # Only finds emails ending with com,org,no,edu or live
        # Regex also works great here as the emails can be found in many different tags, so BeautifulSoup is not necesarry here
        regex = re.compile(
            r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.(com|no|edu|org|live))')
        emails = [match[0] for match in regex.findall(content)]
        return emails

    def find_phone_numbers(self, content: str):
        # I am not using BeautifulSoup for this one because it is simpler to just use a regular expression
        regex = re.compile(
            r'(((\+4[0-9])\s\d{2}\s\d{2}\s\d{2}\s\d{2})|(\d{2}\s\d{2}\s\d{2}\s\d{2})|((?=href=)\"tel:\d{8}\"))')
        phone_numbers = [match[0] for match in regex.findall(content)] # I only want the first capture group in each match
        return phone_numbers
    
    def find_comments(self, content: str):
        regex = re.compile(r'(<!--([a-zA-z0-9\s.-_,]+)-->)')
        comments = [match[1] for match in regex.findall(content)] # I only save the text of the comment
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
        
        most_common_word = self.count_words(unique_words, text_elements)
        return most_common_word
    
    def count_words(self, unique_words: list, text_elements: list):
        highest = 0
        most_common_word = ""
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
        'https://www.vg.no', 1)
    s.start_scraping()
    s.save_result()
    end = time.time()
    print(end-start)

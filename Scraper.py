import requests
import time
import re
import lxml.html
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.start_url = ""
        self.common_words = []
        self.urls = []
        self.phone_numbers = []
        self.emails = []
        self.comments = []
        self.search_results = []
        self.visited_urls = []
        
    
    def start_scraping(self, url: str, depth: int, search_params=[]):
        self.start_url = url
        self.scrape(url, depth, search_params)
    
    def write_to_file(self, input):
        for item in input:
            self.output.write("     {}\n".format(item))
    
    def fetch_html(self, url: str):
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            return res
        except requests.exceptions.ConnectionError as e:
            print(e)
            return None
        except requests.exceptions.TooManyRedirects as e:
            print(e)
            return None

    
    def save_result(self, filename='output.txt'):
        with open(filename, 'w') as output:
            output.write("Start url: {}\n".format(self.start_url))
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


    def scrape(self, url: str, current_depth: int, search_params: list):
        if url in self.visited_urls:
            return
        
        res = self.fetch_html(url)
        if res == None:
            return
        print(url)
        content = res.text
        soup = BeautifulSoup(content, features='lxml')
        
        urls = self.find_urls(soup)

        for param in search_params:
            r =  self.find_custom(content, param)
            if r:
                self.search_results.append(r)

        # All results are formatted tuples (url, list_of_results) and added to the instance variables
        self.urls.append((url, urls))
        phone_numbers = self.find_phone_numbers(content)
        if phone_numbers:
            self.phone_numbers.append((url, phone_numbers))
        emails = self.find_emails(content, url)
        if emails:
            self.emails.append((url, emails))
        comments = self.find_comments(content)
        if comments:
            self.comments.append((url, comments))
        self.common_words.append((url, self.find_common_words(soup)))
        
        self.visited_urls.append(url) # Marks this url as visited
        
        if current_depth == 0:
            return
        else:
            for u in urls:
                self.scrape(u, current_depth - 1, search_params) # Recursively scrape urls when depth > 0

    def find_elements_by_tag(self, url: str, tag: str):
        # Returns all matching tags
        result = self.fetch_html(url)
        if result:
            soup = BeautifulSoup(result.text, features='lxml')
            result = soup.find_all(tag)
        return result
    
    def find_element_by_id(self, url: str, id: str):
        result = self.fetch_html(url)
        if result:
            soup = BeautifulSoup(result.text, features='lxml')
            result = soup.find(id=id).prettify()
        return result
    
    def find_tag(self, url: str, tag: str):
        # Returns the first matching tag
        result = self.fetch_html(url)
        if result:
            soup = BeautifulSoup(result.text, features='lxml')
            result = soup.find(tag)
        return result
    
    def exists(self, url: str, regex: str):
        # Checks if the regular expression exists on the website
        result = self.fetch_html(url)
        if result:
            r = re.compile(regex, flags=re.MULTILINE)
            result = r.search(result.text)
        return bool(result)


    def find_urls(self, soup: BeautifulSoup):
        a_tags = soup.find_all(
            'a', href=re.compile(r'(^(http|https)[^\"]+)(?<!\.pdf)(?<!\.mp4)(?<!\.png)(?<!\.img)$', flags=re.MULTILINE))
        links = [i.get('href') for i in a_tags]
        return links
    
    def find_emails(self, content: str, url: str):
        regex = re.compile(
            r'\b([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', flags=re.MULTILINE)
        emails = regex.findall(content)
        return emails

    def find_phone_numbers(self, content: str):
        regex = re.compile(
            r'\b((\+?4[0-9]\s?)?(\d{2}\s){3}\d{2})\b', flags=re.MULTILINE)
        print(regex.findall(content))
        phone_numbers = [match[0] for match in regex.findall(content)]
        return phone_numbers
    
    def find_comments(self, content: str):
        regex = re.compile(r'<!--(.*)-->', flags=re.MULTILINE)
        comments = regex.findall(content)
        return comments
    
    def find_custom(self, content: str, param: str):
        regex = re.compile(param, flags=re.MULTILINE)
        result = regex.findall(content)
        return result
    
    def find_common_words(self, soup: BeautifulSoup):
        # only interested in actual words, not symbols
        regex = re.compile(r'\b[a-zA-Z0-9.,\-!?]+', flags=re.MULTILINE)
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
    
    def get_stats(self):
        urls = self.urls
        emails = self.emails
        phone_numbers = self.phone_numbers
        total_urls = 0
        total_emails = 0
        total_phone_numbers = 0
        avg_phone_numbers = 0
        for item in urls:
            total_urls += len(item[1])
        avg_urls = round(total_urls / len(urls))
        avg_emails = 0
        if len(emails) > 0:
            for email in emails:
                total_emails += len(email[1])
            avg_emails = round(total_emails / len(emails))
        if (len(phone_numbers) > 0):
            for numbers in phone_numbers:
                total_phone_numbers += len(numbers[1])
            avg_phone_numbers = round(total_phone_numbers / len(phone_numbers))
        averages = [avg_urls, avg_emails, avg_phone_numbers]
        
        return averages
    

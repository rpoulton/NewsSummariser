from urlprocess import *
from HTMLParser import HTMLParser
import requests
from urlparse import urljoin

BASE='https://news.google.com/'
TOP = 'https://news.google.com/news/?ned=us&gl=GB&hl=en'
WORLD='https://news.google.com/news/headlines/section/topic/WORLD?ned=us&hl=en&gl=GB'
USNAT='https://news.google.com/news/headlines/section/topic/NATION?ned=us&hl=en&gl=GB'
BUSN='https://news.google.com/news/headlines/section/topic/BUSINESS?ned=us&hl=en&gl=GB'
TECH='https://news.google.com/news/headlines/section/topic/TECHNOLOGY?ned=us&hl=en&gl=GB'
ENTRTN='https://news.google.com/news/headlines/section/topic/ENTERTAINMENT?ned=us&hl=en&gl=GB'
SPORT='https://news.google.com/news/headlines/section/topic/SPORTS?ned=us&hl=en&gl=GB'
SCIENCE='https://news.google.com/news/headlines/section/topic/SCIENCE?ned=us&hl=en&gl=GB'
HEALTH='https://news.google.com/news/headlines/section/topic/HEALTH?ned=us&hl=en&gl=GB'

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    links = []
    fileComplete = []
    linkChk = 0
    linkCount = 0
    linkReset = 0

    # search for top news items from link
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = urljoin(BASE, value)
                    if 'google.' not in url:
                        self.linkReset += 1
                        if self.linkCount > 0 and self.linkReset < 4:
                            print(url)
                            self.fileComplete.append(url+'\n')
                            self.links.append(url)
                        if self.linkCount > 4:
                            break
                        self.linkChk = 1

    #handle data around specified tag to count how many links are being read in
    def handle_data(self, data):
        if self.linkChk == 0:
            pass
        elif 'More about' in data:
            self.linkCount += 1
            self.linkReset = 0
        elif self.linkCount > 0 and self.linkReset < 1:
            print(data)
            self.fileComplete.append(data+'\n')
            self.linkChk = 0

    def page_links(self):
        return self.links

    def file_complete(self):
        return self.fileComplete

def start(url):
    #find top news links
    print('Finding top news items...')
    source_code = requests.get(url).text
    parser = MyHTMLParser()
    parser.feed(source_code)
    links = parser.links

    print('Compiling news items...')
    process(links)
    fpath = "file.txt"
    fileC=parser.fileComplete
    delete_file_contents(fpath)
    append_file(fpath,fileC,0)
    print('News trimmer process completed.')

start(WORLD)
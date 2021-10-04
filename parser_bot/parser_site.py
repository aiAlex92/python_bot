import requests #upm package(requests)

from lxml.html import document_fromstring #upm package(lxml)
from dateutil import parser
from datetime import datetime

from user_db import moscow_tz

class Article():
    def __init__(self, title, url, authors, timestamp=None):
        self.title = title
        self.url = url
        self.timestamp = timestamp
        self.authors = authors

        self.image_url = None
        self.text = None
    
    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp, tz=moscow_tz)

    def __str__(self):
        human_dt = self.datetime.strftime("%d.%m.%Y, %H:%M:%S")        
        return f"{self.title} | by {', '.join(self.authors)}\n{self.url}\n@ {human_dt}"

    def parse_content(self):
        if self.text and self.image_url:
            return 
        
        response = requests.get(self.url)

        if response.status_code != 200:
            print("Не могу загрузить страницу!")
            return

        html_doc = document_fromstring(response.text)

        content = html_doc.find_class('article-content')[0]

        self.text = content.text_content().strip()
        self.image_url = html_doc.find_class('article__featured-image')[0].get('src').strip()

def parse_techcrunch():
    response = requests.get("https://techcrunch.com")

    if response.status_code != 200:
        print("Не могу загрузить страницу!")
        return

    html_doc = document_fromstring(response.text)

    post_blocks = html_doc.find_class('post-block')

    articles = []

    for pblock in post_blocks:
        link = pblock.find_class('post-block__title__link')[0]
        title = link.text_content().strip()

        url = link.get('href')

        ablock = pblock.find_class('river-byline__authors')[0]

        authors = [ link.text_content().strip() for link in ablock.iter('a') ]

        time_str = pblock.find_class('river-byline__time')[0].get('datetime')
        dt = parser.parse(time_str)

        article = Article(title, url, authors, timestamp=dt.timestamp())
        articles.append(article)

    return articles

if __name__ == '__main__':
    for idx, article in enumerate(parse_techcrunch()):
        print(f"{idx + 1}.", article, end="\n\n")

        article.parse_content()
        print(article.text, article.image_url)
        break
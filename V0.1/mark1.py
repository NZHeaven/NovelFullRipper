#https://realpython.com/beautiful-soup-web-scraper-python/
#https://www.geeksforgeeks.org/python-convert-html-pdf/

import requests
import pdfkit
from bs4 import BeautifulSoup

URL = "https://novelfull.com/i-have-countless-legendary-swords/chapter-{0}.html"
ChapterNumber = 32
page = requests.get(URL.format(ChapterNumber))

while page.status_code != 404:
    soup = BeautifulSoup(page.content,'html.parser')
    chapter = soup.find(id='chapter').prettify()
    f = open("./test.html",'w')
    f.write(str(chapter))
    f.close
    title = "Chapter " + str(ChapterNumber)
    location = "./Chapters/{0}.pdf"
    pdfkit.from_file('test.html', location.format(title))
    ChapterNumber += 1
    page = requests.get(URL.format(ChapterNumber))


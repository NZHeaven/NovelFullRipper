
import requests
from bs4 import BeautifulSoup
import re

uri = r"https://novelfull.com/reincarnation-of-the-strongest-sword-god/chapter-10-abyssal-blade.html"

page = requests.get(uri)
soup = BeautifulSoup(page.content,'html.parser')

Chapter = str(soup.find(id='chapter-content').prettify())
Next_Chaper = str(soup.find(id='next_chap').prettify())

regex = r"(\"/((.|\n)*?).html\")"

matches = re.search(regex,Next_Chaper)
print(matches.group(0))

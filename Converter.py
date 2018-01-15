#from urllib import parse
#querystring = parse.quote_plus('4352,8,')
#print(querystring)
#querystring = parse.unquote_plus('ug%60a%60K%5BQRSAP%0F%0Cvrxb%7CYImO%25%22%2B.%21%2B%12%26%2A%25%2F%2A%2A%2A'+querystring)
#print(querystring)

#actual code
#https://www.magickartenmarkt.de/iajax.php
#from urllib import request
#url = 'https://www.magickartenmarkt.de/iajax.php'
#data = {'args' : 'ug%60a%60K%5BQRSAP%0F%0Cvrxb%7CYImO%25%22%2B.%21%2B%12%26%2A%25%2F%2A%2A%2A4352,11,', 'Referer' : 'https://www.magickartenmarkt.de/Cards/Propaganda'}
#r = request.urlopen(url,data)
#r.read

from requests import Session
import requests
from bs4 import BeautifulSoup
import base64
import time
from Enum.Location import *
import re

# url = 'https://www.magickartenmarkt.de/Cards/Propaganda'
# page = requests.get(url)
# soup = BeautifulSoup(page.text, 'html.parser')
# expansioncontainer = soup.find("div", {"class": "expansionsBox"})
# items = expansioncontainer.find_all("span")
# for item in items:
#     print(item["title"])
#     print(re.compile(r"(?<=\().+?(?=\))").search(item["title"]).group())
# jcp = soup.find("div", {"id": "moreDiv"})["onclick"].split("'")
# print(jcp[1])
# print((jcp[3])[:-1])
# print(soup.find("input", {"name": "totalResults"})["value"])
#print(items)
#print(soup.prettify())
#items = soup.find_all('tr')
#print(items[8:])
#print(type(soup))
#print(soup.tbody)


start = time.time()

session = Session()

session.head('https://www.cardmarket.com/')

response = session.post(
    url='https://www.cardmarket.com/iajax.php',
    data={
    'args' : 'ug%60a%60K%5BQRSAP%0F%0Cvrxb%7CYImO%25%22%2B.%21%2B%12%26%2A%25%2F%2A%2A%2A4352,0,a:1:%7Bs:8:%22idViewer%22;s:7:%221713891%22;%7D'
    },
    headers={
        'Referer': 'https://www.cardmarket.com/de/Magic/Cards/Propaganda'
    }
)


def user(href):
    return href and re.compile("Users").search(href)

def cardlanguage(href):
    return href and re.compile("CardLanguage").search(href)

def cardexpansion(href):
    return href and re.compile("Expansions").search(href)

def standort(onmouseover):
    return onmouseover and re.compile("Artikelstandort").search(onmouseover)

def condition(href):
    return href and re.compile("CardCondition").search(href)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

str = response.text
#remove wrapper
str = str[67:-31]
str = base64.b64decode(str)
soup = BeautifulSoup(str, 'html.parser')

#print(soup.find_all(href=user))

#print(soup.prettify())
items = soup.find_all('tr')
i = 0
for item in items:
    i += 1
    print(item.find(href=user).text)
    print(item.find(href=cardlanguage).span["onmouseover"])
    print(item.find(href=condition).span["onmouseover"])
    print((item.find(href=cardexpansion).span["onmouseover"])[17:-2])
    str = item.find(onmouseover=standort)["onmouseover"]
    for location in Location:
        if location.value != 1:
            print(findWholeWord(location.name)(str))
        else:
            print(findWholeWord(location.name.replace("_", " "))(str))
    print((item.find("td", {"class": "st_price Price"}).div["id"])[5:])
    print(item.find("td", {"class": "st_price Price"}).div.div.text)
    bewertung = item.find("td", {"class": "Seller"})
    print(bewertung)

print(i)
#items = soup.find_all('tr')
#print(items)
#
# # str = response.text
# # str = str[67:-31]
# # str = base64.b64decode(str)
# # print(str)
#
# end = time.time()
# print(end - start)

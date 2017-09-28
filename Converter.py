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

url = 'https://www.magickartenmarkt.de/Cards/Propaganda'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
#print(soup.prettify())
items = soup.find_all('tr')
print(items[8:])

session = Session()

session.head('https://www.magickartenmarkt.de')

response = session.post(
    url='https://www.magickartenmarkt.de/iajax.php',
    data={
    'args' : 'ug%60a%60K%5BQRSAP%0F%0Cvrxb%7CYImO%25%22%2B.%21%2B%12%26%2A%25%2F%2A%2A%2A4352,11,'
    },
    headers={
        'Referer': 'https://www.magickartenmarkt.de/Cards/Propaganda'
    }
)
str = response.text
str = str[67:-31]
str = base64.b64decode(str)
print(str)
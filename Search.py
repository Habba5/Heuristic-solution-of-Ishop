from requests import Session

session = Session()

session.head('https://www.magickartenmarkt.de')

response = session.post(
    url='https://www.magickartenmarkt.de/?mainPage=showSearchResult&searchFor=blubb',
)
str = response.text
print(str)
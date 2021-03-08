import requests
from bs4 import BeautifulSoup


class Upcoming():
    def __init__(self):
        print("fuck thuan")

    def getEvents(self, ticker):
        url = 'https://coinmarketcal.com/en/?form%5Bdate_range%5D=08%2F03%2F2021+-+01%2F08%2F2024&form%5Bkeyword%5D=' + ticker
        headers = {
            'User-Agent': 'My User Agent 1.0'
        }
        r = requests.get(url, headers=headers)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        articles = bsObj.findAll('article')

        response = "";
        for a in articles:
            date = a.find('h5', {'class':'card__date'}).text
            title = a.find('h5', {'class':'card__title'}).text
            link = a.findAll('a', {'class':'link-detail'})[1]['href']

            link = "https://coinmarketcal.com" + link
            response = response + date + ": \t" + title + "\n"+link + "\n"
        return response

import requests
from bs4 import BeautifulSoup


class Upcoming():
    def __init__(self):
        pass

    def getEvents(self, ticker):
        url = 'https://coinmarketcal.com/en/?form%5Bdate_range%5D=31%2F03%2F2021+-+01%2F08%2F2024&form%5Bkeyword%5D={}&form%5Bsort_by%5D=date5'.format(ticker)
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

            r = "<a href='{}'> {}  {}  </a>\n".format(link, date, title)
            response = response + r
        return response

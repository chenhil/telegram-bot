from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .model import quote
import re
import json
from millify import millify, prettify
from bs4 import BeautifulSoup

class CoinMarketCap():
    def __init__(self, symbol):
        self.symbol = symbol

    def getPrice(self):
        apiJSONData = self.getCryptoPriceAPI()

        print(apiJSONData)
        if apiJSONData is None: 
            return
        historialData = self.getHistorialData(apiJSONData["data"][self.symbol][0]["slug"])
        if len(historialData) == 0:
            return

        return quote.Quote(
                symbol = self.symbol,
                price = historialData["price"],
                volume24 = millify(apiJSONData["data"][self.symbol][-1]["quote"]["USD"]["volume_24h"], precision = 2),
                percentChange1h = str(round(apiJSONData["data"][self.symbol][-1]["quote"]["USD"]["percent_change_1h"], 2))+ "%",
                percentChange24h = str(round(apiJSONData["data"][self.symbol][-1]["quote"]["USD"]["percent_change_24h"], 2))+"%",
                percentChange7d = str(round(apiJSONData["data"][self.symbol][-1]["quote"]["USD"]["percent_change_7d"], 2))+"%",
                priceLow = historialData["24hourlow"],
                priceHigh = historialData["24hourhigh"],
                marketCap = millify(apiJSONData["data"][self.symbol][-1]["quote"]["USD"]["market_cap"], precision = 2)
            )

    def getCryptoPriceAPI(self):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        parameters = {
            'symbol': self.symbol,
            'convert':'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '133cf23d-92cb-45eb-8e4b-0a33b858e72d',
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            return 

    def getHistorialData(self, slug):
        url = 'https://coinmarketcap.com/currencies/{}/'.format(slug)
        headers = {
            'Accepts': 'application/json'
        }        
        session = Session()
        session.headers.update(headers)
        data = {}
        try:
            response = session.get(url)
            # data = json.loads(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            prices = soup.find_all('span', attrs={'class': re.compile('^highLowValue.*')})
            priceValue = soup.find_all('div', attrs={'class': re.compile('^priceValue.*')})[0]
            data["24hourlow"] = prices[0].text
            data["24hourhigh"] = prices[1].text
            data["price"] = priceValue.text
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)    
        return data
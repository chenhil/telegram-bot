from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import re, json
from millify import millify, prettify
from bs4 import BeautifulSoup
import configparser

class IEXCloud():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        self.apiKey = config['iexcloud']['apiKey']
        self.baseUrl = 'https://cloud.iexapis.com/v1'
        self.stockQuote = '/stock/{}/quote/quote?token={}'


    def getPrice(self, symbol):
        response = {}
        data = self._getStockPriceAPI(symbol)

        response["symbol"] = data["symbol"]
        response["company"] = data["companyName"]
        response["open"] = data["open"]
        response["low"] = data["low"]
        response["high"] = data["high"]
        if data['isUSMarketOpen'] is True:
            response['price'] = data['iexRealtimePrice']
        else:
            response['price'] = data['extendedPrice']
        response['volume'] = millify(data['volume'], precision = 2)
        response['avg volume'] = millify(data['avgTotalVolume'], precision = 2)
        response['52weekhigh'] = data['week52High']
        response['52weeklow'] = data['week52Low']
        response['change'] = data['change']
        response['changePercent'] = str(round(float(data['changePercent']) * 100, 2)) + "%"
        response['extendedChange'] = data['extendedChange']
        response['extendedChangePercent'] = str(round(float(data['extendedChangePercent']) * 100, 2)) + "%"
        response['isUSMarketOpen'] = data['isUSMarketOpen']

        return response

    def _getStockPriceAPI(self, symbol):
        url = self.baseUrl + self.stockQuote.format(symbol, self.apiKey)
        headers = {
            'Accepts': 'application/json',
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url)
            print(response.status_code)
            print(response)
            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            else:
                print(response)
                raise Exception('Unable to find symbol {}'.format(symbol))
        except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
            print(e)
            raise e 

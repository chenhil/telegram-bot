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
        # apiJSONData = self._getCryptoPriceAPI(symbol)
        # if apiJSONData is None or apiJSONData["status"]["error_message"] is not None: 
        #     return response
        # historialData = self.getHistorialData(apiJSONData["data"][symbol][0]["slug"])
        # if len(historialData) == 0:
        #     return response

        # response["symbol"] = symbol
        # response["price"] = historialData["price"]
        # response["volume24"] = millify(apiJSONData["data"][symbol][-1]["quote"]["USD"]["volume_24h"], precision = 2)
        # response["percentChange1h"] = str(round(apiJSONData["data"][symbol][-1]["quote"]["USD"]["percent_change_1h"], 2))+ "%"
        # response["percentChange24h"] = str(round(apiJSONData["data"][symbol][-1]["quote"]["USD"]["percent_change_24h"], 2))+"%"
        # response["percentChange7d"] = str(round(apiJSONData["data"][symbol][-1]["quote"]["USD"]["percent_change_7d"], 2))+"%"
        # response["priceLow"] = historialData["24hourlow"]
        # response["priceHigh"] = historialData["24hourhigh"]
        # response["marketCap"] = millify(apiJSONData["data"][symbol][-1]["quote"]["USD"]["market_cap"], precision = 2)
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
            if response.status_code == 200:
                data = json.loads(response.text)
                return data
            else:
                raise Exception('Unable to find symbol {}'.format(symbol))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise e 


iexCloud = IEXCloud().getPrice("gme")
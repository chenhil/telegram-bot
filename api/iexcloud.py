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


    def getPrice(self, symbol):
        response = {}
        apiJSONData = self._getCryptoPriceAPI(symbol)
        if apiJSONData is None or apiJSONData["status"]["error_message"] is not None: 
            return response
        historialData = self.getHistorialData(apiJSONData["data"][symbol][0]["slug"])
        if len(historialData) == 0:
            return response

        response["symbol"] = symbol
        response["price"] = historialData["price"]
        response["volume24"] = millify(apiJSONData["data"][symbol][-1]["quote"]["USD"]["volume_24h"], precision = 2)
        response["percentChange1h"] = str(round(apiJSONData["data"][symbol][-1]["quote"]["USD"]["percent_change_1h"], 2))+ "%"
        response["percentChange24h"] = str(round(apiJSONData["data"][symbol][-1]["quote"]["USD"]["percent_change_24h"], 2))+"%"
        response["percentChange7d"] = str(round(apiJSONData["data"][symbol][-1]["quote"]["USD"]["percent_change_7d"], 2))+"%"
        response["priceLow"] = historialData["24hourlow"]
        response["priceHigh"] = historialData["24hourhigh"]
        response["marketCap"] = millify(apiJSONData["data"][symbol][-1]["quote"]["USD"]["market_cap"], precision = 2)
        return response

    def _getCryptoPriceAPI(self, symbol):
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
        parameters = {
            'symbol': symbol,
            'convert':'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.apiKey,
        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise e 

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
            raise e
        return data
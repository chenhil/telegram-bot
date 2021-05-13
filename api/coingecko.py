from pycoingecko import CoinGeckoAPI
from millify import millify, prettify
import logging, time

class CoinGecko():
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def getPrice(self, symbol):
        responseJson = self.getCoinById(symbol)
        response = self.cg.get_price(symbol, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')

        responseJson['volume24'] = millify(response[symbol]['usd_24h_vol'], precision = 2)
        return responseJson

    def getCoinData(self, symbol):
        return self.cg.get_coin_by_id(id = symbol['id'], localization = 'false', tickers = 'true', market_data = 'true')
         
    def getCoinById(self, symbol):
        response = self.cg.get_coin_by_id(symbol, localization = 'false', developer_data='false', community_data='false')
        responseJson = {}
        responseJson["symbol"] = response['symbol'].upper()
        responseJson["name"] = response['name'].upper()
        responseJson['price'] = "$"+prettify(str(response["market_data"]['current_price']['usd']))
        responseJson["marketCap"] = millify(response["market_data"]['market_cap']['usd'], precision = 2)
        if len(response["market_data"]["price_change_percentage_1h_in_currency"]) == 0 or "usd" not in response["market_data"]["price_change_percentage_1h_in_currency"]:
            responseJson['percentChange1h'] = "?"
        else: 
            responseJson['percentChange1h'] = str(round(response["market_data"]["price_change_percentage_1h_in_currency"]["usd"], 2))+ "%"
        responseJson['percentChange24h'] = str(round(response["market_data"]["price_change_percentage_24h"], 2))+ "%"
        responseJson['percentChange7d'] = str(round(response["market_data"]["price_change_percentage_7d"], 2))+ "%"
        responseJson["priceLow"] = "$" + prettify(str(response["market_data"]['low_24h']['usd']))
        responseJson["priceHigh"] = "$" + prettify(str(response["market_data"]['high_24h']['usd']))
        responseJson["allTimeHigh"] = "$" + prettify(str(response["market_data"]['ath']['usd']))
        return responseJson
        
    def getCoinList(self):
        return self.cg.get_coins_list()
    
    def getMarketData(self):
        try:
            coinMarketData = dict()
            coinMarketData['usd'] = self._chunks(self._getMarketData("usd"), 10)
            coinMarketData['btc'] = self._chunks(self._getMarketData("btc"), 10)
            coinMarketData['eth'] = self._chunks(self._getMarketData("eth"), 10)
            return coinMarketData
        except Exception as e:
            raise e

    def _getMarketData(self, vsCurrency):
        try:
            data = self.cg.get_coins_markets(vs_currency = vsCurrency, price_change_percentage='24h,7d,30d')
            return data
        except Exception as e:
            logging.error(e)
            raise e

    def _chunks(self, l, n): return [l[x: x+n] for x in range(0, len(l), n)]
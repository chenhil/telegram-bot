from pycoingecko import CoinGeckoAPI
from millify import millify, prettify

class CoinGecko():
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def getPrice(self, symbol):
        responseJson = self.getCoinById(symbol)
        response = self.cg.get_price(symbol, vs_currencies='usd', include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')

        responseJson['volume24'] = millify(response[symbol]['usd_24h_vol'], precision = 2)
        return responseJson
    
    def getCoinById(self, symbol):
        response = self.cg.get_coin_by_id(symbol)
        responseJson = {}

        responseJson["symbol"] = response['symbol'].upper()
        responseJson['price'] = "$"+prettify(str(response["market_data"]['current_price']['usd']))
        responseJson["marketCap"] = millify(response["market_data"]['market_cap']['usd'], precision = 2)
        responseJson['percentChange1h'] = str(round(response["market_data"]["price_change_percentage_1h_in_currency"]["usd"], 2))+ "%"
        responseJson['percentChange24h'] = str(round(response["market_data"]["price_change_percentage_24h"], 2))+ "%"
        responseJson['percentChange7d'] = str(round(response["market_data"]["price_change_percentage_7d"], 2))+ "%"
        responseJson["priceLow"] = "$" + prettify(str(response["market_data"]['low_24h']['usd']))
        responseJson["priceHigh"] = "$" + prettify(str(response["market_data"]['high_24h']['usd']))
        responseJson["allTimeHigh"] = "$" + prettify(str(response["market_data"]['ath']['usd']))
    
        return responseJson
        
    
    def getCoinList(self, symbol):
        data = self.cg.get_coins_list()
        for item in data:
            if symbol.upper() == item['name'].upper() or symbol.upper() == item['symbol'].upper():
                return item
        return None
import logging
import requests
import json

class CoinPaprika():
    Coins = dict()

    def __init__(self):
        self.baseUrl = 'https://api.coinpaprika.com/v1/'
        if len(self.Coins) == 0:
            self._getAllCoins()
    
    def getTweets(self, symbol):
        symbol = self.Coins[symbol]
        api_url = f'{self.baseUrl}coins/{symbol}/twitter'
        return self._request(api_url)

    def _getAllCoins(self):
        api_url = f'{self.baseUrl}coins'
        response = self._request(api_url)
        for coin in response:
            self.Coins[coin['symbol']] = coin['id']

    def _request(self, url):
        try:
            self.response = requests.get(url)
            self.response.raise_for_status()
            return json.loads(self.response.content.decode('utf-8'))
        except Exception as e:
            logging.error(e)
            raise e
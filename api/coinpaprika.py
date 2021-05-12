import logging
import requests
import json

class CoinPaprika():
    def __init__(self):
        self.baseUrl = 'https://api.coinpaprika.com/v1/'
    
    def getTweets(self, symbol):
        api_url = f'{self.baseUrl}coins/{symbol}/twitter'
        return self._request(api_url)

    def getCoinList(self):
        coins = dict()
        api_url = f'{self.baseUrl}coins'
        response = self._request(api_url)
        for coin in response:
            coins[coin['symbol']] = coin['id']
        return coins

    def _request(self, url):
        try:
            self.response = requests.get(url)
            self.response.raise_for_status()
            return json.loads(self.response.content.decode('utf-8'))
        except Exception as e:
            logging.error(e)
            raise e

import configparser
import logging
import requests
import json

class CryptoPanic():

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        self.apiKey = config['cryptopanic']['apiKey']
        self.baseUrl = 'https://cryptopanic.com/api/v1/posts/'


    def get_posts(self):
        url = f"{self.baseUrl}?auth_token={self.apiKey}"
        return self._request(url)

    def get_filtered_news(self, filter):
        """filter=(rising|hot|bullish|bearish|important|saved|lol)"""
        url = f"{self.baseUrl}?auth_token={self.apiKey}&filter={filter}"
        return self._request(url)


    def _request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8'))
        except Exception as e:
            raise e        
import requests
from bs4 import BeautifulSoup

#TODO, need store connection in upper
import os
import psycopg2

class Coinstats():

    def getAsset(self, record):
        return self.getAssetLink(record)

    def getAssetLink(self, url):
        r = requests.get(url)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        totalAsset = bsObj.find('span', {'class': 'main-price'})['title']
        response = 'Total: ' + str(totalAsset) + '\n'

        coins = bsObj.find('div', {'class': 'coins-container'}).ul

        for coin in coins:
            currency = coin.find('span', {'class': 'table-row'}).text
            amount = coin.find('span', {'class': 'primary-nav'}).text
            response = response + currency + ": " +  amount + "\n"

        return response


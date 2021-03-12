import requests
from bs4 import BeautifulSoup

#TODO, need store connection in upper
import os
import psycopg2

class Coinstats():
    def __init__(self):
        url = 'postgres://whkrhdwpenhhym:598bb25bd018891284d02f939948b0b25a06df4508c251143f98fe1671a12f43@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d5i6go6su3sf1h'
        self.connection = psycopg2.connect(url,sslmode='require')
        pass

    def getAsset(self, user_id, asset_id):
        cursor = self.connection.cursor()

        query = "SELECT profile_link  FROM Asset  WHERE user_id = '{}' and asset_id = '{}';".format(user_id, asset_id)
        cursor.execute(query)
        record = cursor.fetchone()[0]
        self.connection.close()
        return self.getAssetLink(record)

    def saveAsset(self, user_id, asset_id, link):
        try:
            cursor = self.connection.cursor()

            #delete if exist
            query = "DELETE FROM ASSET WHERE USER_ID = '{}' AND ASSET_ID = '{}';".format(user_id, asset_id)
            cursor.execute(query)

            #insert
            query = "INSERT INTO Asset(user_id, asset_id, profile_link) VALUES ('{}', '{}', '{}')".format(user_id, asset_id, link)
            cursor.execute(query)
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print(e)



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


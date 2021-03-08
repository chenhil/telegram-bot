import requests
from bs4 import BeautifulSoup


class Coinstats():
    def __init__(self):
        print("fuck thuan")

    def getAsset(self, user):
        if(user == '@b0sssie'):
            url = 'https://coinstats.app/p/LQZZXg'
            r = requests.get(url)
            bsObj = BeautifulSoup(r.text, 'html.parser')
            totalAsset = bsObj.find('span', {'class': 'main-price'})['title']
            return "Total: " + totalAsset

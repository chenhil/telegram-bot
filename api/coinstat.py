import requests
from bs4 import BeautifulSoup


class Coinstats():
    def __init__(self):
        print("fuck thuan")

    def getAsset(self, user):
        url = self.findUserData(user)
        r = requests.get(url)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        totalAsset = bsObj.find('span', {'class': 'main-price'})['title']

        response = "Total: " + totalAsset + "\n"

        coins = bsObj.find('div', {'class': 'coins-container'}).ul

        for coin in coins:
            currency = coin.find('span', {'class': 'table-row'}).text
            amount = coin.find('span', {'class': 'primary-nav'}).text
            response = response + currency + ": " +  amount + "\n"

        return response

    def saveUser(self, user, link):
        self.removeUserData(user)
        with open("./config/coinstats.txt", "a") as myfile:
            myfile.write(user + ' ' + link+'\n')

    def findUserData(self, user):
        try:
            with open("./config/coinstats.txt") as fp:
                for line in fp:
                    line = line.strip("\n")
                    line = line.split()
                    if line[0] == user:
                        return line[1]
        except Exception as e:
            print(e)

    def removeUserData(self, user):
        a_file = open("./config/coinstats.txt", "r")
        lines = a_file.readlines()
        a_file.close()

        new_file = open("./config/coinstats.txt", "w")
        for line in lines:
            if line.split()[0] != user:
                new_file.write(line)
        new_file.close()



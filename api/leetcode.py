import configparser
import logging
import requests
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

class Leetcode():
    def getStats(self, username):
        data = '''
        {
            "query": "query getUserProfile($username: String!, $limit: Int!) { recentAcSubmissionList(username: $username, limit: $limit) { id title titleSlug timestamp} matchedUser(username: $username) { submitStats { acSubmissionNum { difficulty count submissions } totalSubmissionNum { difficulty count submissions } } } } ",
            "variables": {
                "username": "%s",
                "limit": 6
            }
        }'''% (username)
        response = requests.post("https://leetcode.com/graphql/", data, headers = {"Content-Type": "application/json", "Referer": "https://leetcode.com/{}".format(username)} )
        return self.getMarkdown(username, response)

    def getMarkdown(self, username, response):
        tz = pytz.timezone('US/Pacific')

        data = response.json()['data']
        user = data['matchedUser']['submitStats']['acSubmissionNum']
        # recent = data['recentAcSubmissionList']
        recent = []
        for ans in data['recentAcSubmissionList']: 
            dt = datetime.fromtimestamp(int(ans['timestamp']), tz)
            recent.append(ans['title'] + " \n" + "Submitted: " + dt.strftime('%I:%M%p %m-%d-%Y') + "\n")

        return (str("```") + "\n"
        + "Leetcode Status: {}\n\n".format(username)
        + "Easy:   {}\n".format(user[1]["count"])
        + "Medium: {}\n".format(user[2]["count"])
        + "Hard:   {}\n".format(user[3]["count"])
        + "\n\n"
        + "Recently Completed: \n\n"
        + "".join([str(item) + "\n" for item in recent]) 
        + "\n" + str("```"))

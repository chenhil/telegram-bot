from telegram import ParseMode
from plugin import PluginImpl, Keyword
import requests
from bs4 import BeautifulSoup
import json

class Gas(PluginImpl):
    def get_cmds(self):
        return ["gas"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        headers = {'User-Agent': 'My User Agent 1.0'}
        response = requests.get('https://www.gasnow.org/api/v3/gas/price?utm_source=soulmachine', headers=headers)
        obj = response.json()
        response = ""
        if obj['code'] == 200:
            gas = obj['data']
            for k, v in gas.items():
                if k == 'timestamp':
                   continue
                price = int(v / 1000000000)
                price = str(price) + " Gwei"
                response = response + k + ": " + price + '\n'

        update.message.bot.send_message(chat_id = update.effective_chat.id,
            text=self._getMarkdown(response), parse_mode=ParseMode.MARKDOWN_V2)

    def _getMarkdown(self, response):
        if response is None:
            return response
        response = response.replace(".", "\\.").replace("\-", "\\-").replace("|", "\\|")
        response = response.replace("(", "\\(").replace(")", "\\)").replace("!", "\\!")
        response = response.replace("@", "\\@").replace("#", "\\#").replace("$", "\\!")
        response = response.replace("%", "\\%").replace("*", "\\*")
        response = response.replace("+", "\\+").replace("[", "\\[").replace("]", "\\]")
        return response



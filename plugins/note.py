from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.coinstat import Coinstats
from api.count import count
import requests
from bs4 import BeautifulSoup

class Note(PluginImpl):
    def get_cmds(self):
        return ["note", "n", "notes"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        url = 'http://www.itextpad.com/nvzVwBUJ0T'
        headers = {'User-Agent': 'My User Agent 1.0'}
        r = requests.get(url, headers=headers)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        notes = bsObj.find('textarea', {'name':'padText'}).text
        update.message.bot.send_message(chat_id = update.effective_chat.id,
            text=self._getMarkdown(notes), parse_mode=ParseMode.MARKDOWN_V2)

    def _getMarkdown(self, response):
        if response is None:
            return response
        response = response.replace(".", "\\.").replace("|", "\\|")
        response = response.replace("(", "\\(").replace(")", "\\)").replace("!", "\\!")
        response = response.replace("@", "\\@").replace("#", "\\#").replace("$", "\\!")
        response = response.replace("%", "\\%").replace("*", "\\*").replace("-", "\\-")
        response = response.replace("\+", "\\+").replace("[", "\\[").replace("]", "\\]")
        return response

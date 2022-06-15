from telegram import ParseMode
from plugin import PluginImpl, Keyword
import util.emoji as emo
import random
from api.leetcode import Leetcode
import datetime

class Fear(PluginImpl):

    def get_cmds(self):
        return ["fear"]

    def get_action(self, update, context):
        timestamp = datetime.datetime.now().isoformat()
        url = "https://alternative.me/crypto/fear-and-greed-index.png"
        pic_url = '{0}?a={1}'.format(url, timestamp)
        update.message.bot.send_photo(chat_id = update.effective_chat.id, photo=pic_url)

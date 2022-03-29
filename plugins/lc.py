from telegram import ParseMode
from plugin import PluginImpl, Keyword
import util.emoji as emo
import random
from api.leetcode import Leetcode

class Lc(PluginImpl):

    def get_cmds(self):
        return ["lc"]

    def get_action(self, update, context):
        username = context.args[0]
        response = Leetcode().getStats(username)
        update.message.bot.send_message(chat_id = update.effective_chat.id, 
        text=response, parse_mode=ParseMode.MARKDOWN_V2)

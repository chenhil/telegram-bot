from telegram import ParseMode
from plugin import PluginImpl, Keyword
import util.emoji as emo
import telegram.dice

class Dice(PluginImpl):
    def get_cmds(self):
        return ["roll"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        context.bot.send_dice(emoji='🎲', chat_id=update.effective_chat.id)

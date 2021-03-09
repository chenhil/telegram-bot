from telegram import ParseMode
from plugin import PluginImpl, Keyword
import util.emoji as emo
import telegram.dice

class Dice(PluginImpl):
    def get_cmds(self):
        return ["roll"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if len(context.args) == 1 and context.args[0] == 2:
            context.bot.send_dice(emoji='🎲', chat_id=update.effective_chat.id)

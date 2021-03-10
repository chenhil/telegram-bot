from telegram import ParseMode
from plugin import PluginImpl, Keyword
import util.emoji as emo
import random


class Dumb(PluginImpl):

    def get_cmds(self):
        return ["dumb"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        person_tag = ' '.join(context.args)
        text_message = ''.join(random.choice((str.upper, str.lower))(c) for c in update.message.reply_to_message.text) if update.message.reply_to_message is not None else person_tag
        update.message.bot.send_photo(chat_id = update.effective_chat.id, photo='https://i.imgflip.com/4/1p9wjx.jpg', caption=text_message)
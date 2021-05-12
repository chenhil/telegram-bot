from telegram import ParseMode
from plugin import PluginImpl
from api.s3 import S3
import random

class Meme(PluginImpl):

    def get_cmds(self):
        return ["meme"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        randomMeme = S3().getFile()
        if '.mp4' in randomMeme:
            update.message.bot.send_animation(chat_id = update.effective_chat.id, animation=randomMeme)
        else:
            update.message.bot.send_photo(chat_id = update.effective_chat.id, photo=randomMeme)
    
    def get_usage(self):
        return f"`/{self.get_cmds()[0]}`\n"

    def get_description(self):
        return "Send a random meme"

    def get_category(self):
        return None

from telegram import ParseMode
from plugin import PluginImpl
from api.count import count
import random

class Meme(PluginImpl):

    def get_cmds(self):
        return ["meme"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        with open('./config/file_id.txt', "r") as f:
            lines = [line.rstrip() for line in f]
            filename = random.choice(lines)
            print(filename)
            if "document" in filename:
                update.message.bot.send_animation(chat_id = update.effective_chat.id, animation=filename.replace("document_", ""))
            else:
                update.message.bot.send_photo(chat_id = update.effective_chat.id, photo=filename.replace("photo_", ""))
    
    def get_usage(self):
        return f"`/{self.get_cmds()[0]}`\n"

    def get_description(self):
        return "Send a random meme"

    def get_category(self):
        return None

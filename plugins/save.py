from telegram import ParseMode
from plugin import PluginImpl
import random

class Save(PluginImpl):
    def get_cmds(self):
        return ["save"]

    @PluginImpl.save_data
    @PluginImpl.send_typing
    def get_action(self, update, context):
        if update.message.reply_to_message is None:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        fileName = ""
        if len(update.message.reply_to_message.photo) != 0:
            photo = update.message.reply_to_message.photo[-1]
            newFile = update.message.bot.get_file(photo.file_id)
            fileName = "photo_" + photo.file_id
        elif update.message.reply_to_message.document != None:
            document = update.message.reply_to_message.document
            newFile = update.message.bot.get_file(document.file_id)
            fileName = "document_" + document.file_id
        with open("./config/file_id.txt", "a") as myfile:
            myfile.write(fileName + "\n")
        
    def get_usage(self):
        return f"`reply to a image/gif with /{self.get_cmds()[0]}`\n"

    def get_description(self):
        return "Save a meme"

    def get_category(self):
        return None

from telegram import ParseMode
from plugin import PluginImpl
from api.s3 import S3
import os
import random, logging


class Save(PluginImpl):
    def get_cmds(self):
        return ["save"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if update.message.reply_to_message is None:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        if len(update.message.reply_to_message.photo) != 0:
            self._savePhoto(update)
        elif update.message.reply_to_message.document != None:
            self._saveDocument(update)
        
    def _savePhoto(self, update):
        photo = update.message.reply_to_message.photo[-1]
        newFile = update.message.bot.get_file(photo.file_id)
        fileName = newFile.download()
        S3().uploadFile(fileName)
        # Delete local file after upload
        self._removeFile(fileName)

    def _saveDocument(self, update):
        document = update.message.reply_to_message.document
        newFile = update.message.bot.get_file(document.file_id)
        fileName = newFile.download()
        S3().uploadFile(fileName)
        newFile.download(fileName)
        # Delete local file after upload
        self._removeFile(fileName)        

    def get_usage(self):
        return f"`reply to a image/gif with /{self.get_cmds()[0]}`\n"

    def get_description(self):
        return "Save a meme"

    def _removeFile(self, fileName):
        os.remove(fileName)

    def get_category(self):
        return None

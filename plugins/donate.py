from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.count import count

class Donate(PluginImpl):

    def get_cmds(self):
        return ["donate"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        text_message = 'Please consider donating!'
        update.message.bot.send_photo(chat_id = update.effective_chat.id, photo='https://media.discordapp.net/attachments/586050855145570306/819392492095930408/AQXwhxksytM9AAAAAElFTkSuQmCC.png', caption=text_message)

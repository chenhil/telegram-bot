from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.plex import PlexAPI

class Plex(PluginImpl):
    def get_cmds(self):
        return ["plex"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        response = PlexAPI().getMarkdown()
        update.message.bot.send_message(chat_id = update.effective_chat.id, 
        text=response, parse_mode=ParseMode.MARKDOWN_V2)

from telegram import ParseMode
from plugin import PluginImpl, Keyword

class Donator(PluginImpl):
    def get_cmds(self):
        return ["d", "donator"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        response = """
            cashapp: $b0ssie
            1. @i123sb - $75 cashapp
            2. @ScrubMasterAsh - $36 cashapp
            3. @icahnn  - $35 cashapp
            4. @GQvisions - $10 cashapp
            5. @Karan - $1 cashapp
        """
        print(response)

        try:
            update.message.bot.send_message(chat_id = update.effective_chat.id,
                text=self._getMarkdown(str(response)), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print(e)

    def _getMarkdown(self, response):
        if response is None:
            return response
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

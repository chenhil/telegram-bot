from telegram import ParseMode
from plugin import PluginImpl, Keyword


class Donator(PluginImpl):
    def get_cmds(self):
        return ["donator", "list", "top"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        response = """
        Donation List
        \n1. @i123sb - $75 cashapp
        \n2. @ScrubMasterAsh - $36 cashapp
        \n3. @icahnn  - $35 cashapp
        \n4. @GQvisions - $15 cashapp
        \n5. @Karan - $1 cashapp
        """
        print(response)

        try:
            update.message.bot.send_message(chat_id=update.effective_chat.id,
                                            text=self._getMarkdown(str(response)), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print(e)

    def _getMarkdown(self, response):
        if response is None:
            return response
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

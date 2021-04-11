from telegram import ParseMode
from plugin import PluginImpl, Keyword


class Donator(PluginImpl):
    def get_cmds(self):
        return ["donator", "list", "top", "dl"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        response = """
        Donation List
        1. @FixmerT - $511 (0.3 eth)
        2. @ScrubMasterAsh - $86 cashapp
        3. @icahnn  - $76 cashapp
        4. @i123sb - $75 cashapp
        5. @GQvisions - $40 cashapp
        6. @ldealized - $10 cashapp
        7. @Karan - $1 cashapp
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
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|").replace("(","\\(").replace(")","\\)")

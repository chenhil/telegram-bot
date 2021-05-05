from telegram import ParseMode
from plugin import PluginImpl, Keyword


class Donate(PluginImpl):
    def get_cmds(self):
        return ["d", "donate"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        response = """
        Please consider donating to support the development and upkeep of this bot.
        \ncashapp: $b0ssie
        \nBNB: 0xF6c07cE91e44f8A9E88Af880BEFd3bcf2b492F22
        \nEth: 0xcc5BC3Fe73e8CD00B30C889f6b685a3de1D313ce
        """

        try:
            update.message.bot.send_message(chat_id=update.effective_chat.id,
                                            text=self._getMarkdown(str(response)), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print(e)

    def _getMarkdown(self, response):
        if response is None:
            return response
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

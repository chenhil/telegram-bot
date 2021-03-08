from telegram import ParseMode
from plugin import PluginImpl, Keyword
from telegram import ParseMode
from api.coinstat import Coinstats

class CoinstatAsset(PluginImpl):
    def get_cmds(self):
        return ["asset"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            response = Coinstats().getAsset(self, context.args[0])
            print(response)
            update.message.bot.send_message(chat_id = update.effective_chat.id,
            text=self._getMarkdown(response), parse_mode=ParseMode.MARKDOWN_V2)

        except Exception as e:
            return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)


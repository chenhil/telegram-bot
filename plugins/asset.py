from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.coinstat import Coinstats

class Asset(PluginImpl):
    def get_cmds(self):
        return ["a"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        user = update.message.from_user.username
        """
        if len(context.args) != 1:
            update.message.reply_text(  
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        """
        if len(context.args) == 0:
            self.getTotalAsset(user, update)
        else:
            if context.args[0] == 'save':
                self.saveUser(user, context.args[1])
            else:
                user = context.args[0].replace("@","")
                self.getTotalAsset(user, update)


    def _getMarkdown(self, response):
        if response is None:
            return response
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def getTotalAsset(self, user, update):
        try:
            response = Coinstats().getAsset(user)
            update.message.bot.send_message(chat_id = update.effective_chat.id,
            text=self._getMarkdown(response), parse_mode=ParseMode.MARKDOWN_V2)

        except Exception as e:
            print(e)
            #return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)

    def saveUser(self, user, link):
        try:
            Coinstats().saveUser(user, link)
        except Exception as e:
            print(e)
            #return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)

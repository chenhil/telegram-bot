from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.coinstat import Coinstats

class Asset(PluginImpl):
    def get_cmds(self):
        return ["a", "asset"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        userId = update.message.from_user.id
        user = update.message.from_user.username

        response = "@{} Profile ".format(user)

        if len(context.args) == 0:
            response = response + "1" + "\n"
            response = response + self.getAsset(userId, 1)
            update.message.bot.send_message(chat_id = update.effective_chat.id,
                text=self._getMarkdown(str(response)), parse_mode=ParseMode.MARKDOWN_V2)
        elif len(context.args) == 1:
            response = response + context.args[0] + "\n"
            response = response + self.getAsset(userId, context.args[0])
            update.message.bot.send_message(chat_id = update.effective_chat.id,
                text=self._getMarkdown(str(response)), parse_mode=ParseMode.MARKDOWN_V2)
        elif context.args[0] == 'save':
            response = self.saveAsset(userId, 1, context.args[1])
        elif context.args[1] == 'save':
            response = self.saveAsset(userId, context.args[0], context.args[2])


    def getAsset(self, user_id, asset_id):
        response = Coinstats().getAsset(user_id, asset_id)
        return response

    def saveAsset(self, user_id, asset_id, link):
        response = Coinstats().saveAsset(user_id, asset_id, link)
        return response


    def _getMarkdown(self, response):
        if response is None:
            return response
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

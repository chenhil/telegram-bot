from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.upcoming import Upcoming as News

class Upcoming(PluginImpl):
    def get_cmds(self):
        return ["upcoming", "up"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(  
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        self.getEvents(update, context.args[0])

    def _getMarkdown(self, response):
        if response is None:
            return response
        response = response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")
        response = response.replace(")", "\\)").replace("(","\\(")
        return response


    def getEvents(self, update, ticker):
        try:
            response = News().getEvents(ticker)
            update.message.bot.send_message(chat_id = update.effective_chat.id,
            text=response, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


        except Exception as e:
            print(e)
            #return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)


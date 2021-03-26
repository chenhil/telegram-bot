from telegram import ParseMode
from plugin import PluginImpl
from api.coingecko import CoinGecko
from datetime import datetime
import logging, traceback 


class Bio(PluginImpl):

    def get_cmds(self):
        return ["bio"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            coinSymbol = CoinGecko().getCoinList(context.args[0])
            coinData = CoinGecko().getCoinData(coinSymbol)
            output = "<b>" + coinSymbol['id'] + " - " + coinSymbol['symbol'] + "</b>\n\n"
            output += coinData['description']['en']
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=output, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

        except Exception as e:
            logging.error(e)
            logging.error(traceback.print_exc())
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)
    
    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <crypto>`\n"

    def get_description(self):
        return "Get bio info related to a coin"


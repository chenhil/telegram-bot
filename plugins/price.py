from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.coinmarketcap import CoinMarketCap
import random

class Price(PluginImpl):

    def get_cmds(self):
        return ["p"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            response = CoinMarketCap().getPrice(context.args[0].upper())
            print(response)
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=self._getMarkdown(response), parse_mode=ParseMode.MARKDOWN_V2)

        except Exception as e:
            return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <symbol>`\n"

    def get_description(self):
        return "Get the current price of a cryto/stock"

    def get_category(self):
        return None

    def _getMarkdown(self, response):
        output = (str('```') + "\n" + self._getSymbol(response) + "\n" 
        + self._getPercentChange1h(response) + "\n" 
        + self._getPercentChange24h(response) + "\n" 
        + self._getPercentChange7d(response) + "\n" 
        + self._getPriceLow(response) + "\n"
        + self._getPriceHigh(response) + "\n"
        + self._getVolume(response) + "\n"
        + self._getMarketCap(response) + "\n"
        + str('```'))

        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _getSymbol(self, response):
        return "{}          {}".format(response['symbol'], response['price'])

    def _getPercentChange1h(self, response):
        return "1h:          {}".format(response['percentChange1h']).replace(" -", "-")
    
    def _getPercentChange24h(self, response):
        return "24h:         {}".format(response['percentChange24h']).replace(" -", "-")

    def _getPercentChange7d(self, response):
        return "7d:          {}".format(response['percentChange7d']).replace(" -", "-")
    
    def _getVolume(self, response):
        return "Volume24h:   {}".format(response['volume24'])

    def _getPriceLow(self, response):
        return "24L          {}".format(response['priceLow'])
    
    def _getPriceHigh(self, response):
        return "24H:         {}".format(response['priceHigh'])

    def _getMarketCap(self, response):
        return "Market Cap:  {}".format(response['marketCap'])
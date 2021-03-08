from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.iexcloud import IEXCloud
import util.emoji as emo
import random

class Stockprice(PluginImpl):

    def get_cmds(self):
        return ["sp"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            response = IEXCloud().getPrice(context.args[0].upper())
            print(response)
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=self._getMarkdown(response), parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print(e)
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <stock ticker>`\n"

    def get_description(self):
        return "Get the current price of a stock"

    def get_category(self):
        return None

    def _getMarkdown(self, response):
        output = (str('```') + "\n" + self._getSymbol(response) + "\n" 
        + self._getPriceToday(response) + "\n"
        + self._getPriceExtended(response) + "\n"
        + self._getOpen(response) + "\n"
        + self._getPriceHigh(response) + "\n"
        + self._getPriceLow(response) + "\n"
        + self._getVolume(response) + "\n"
        + self._getAvgVolume(response) + "\n"
        + self._get52WKHigh(response) + "\n"
        + self._get52WKLow(response) + "\n"
        + str('```'))
        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _getSymbol(self, response):
        return "{0:<10} {1:<10}".format(response['symbol'], response['price'])

    def _getPriceToday(self, response):
        arrow = ""
        if "-" in str(response['change']):
            arrow = emo.DOWN_ARROW
            response['change'] = response['change'] * -1
        else:
            arrow = emo.UP_ARROW
        change = str(response['change']) + " (" + str(response['changePercent']) + ")"
        return "{0:<10} {1:>8} {2:<4}".format("Today: ", change, arrow)

    def _getPriceExtended(self, response):
        if response['isUSMarketOpen'] is False:
            arrow = ""
            if "-" in str(response['extendedChange']):
                arrow = emo.DOWN_ARROW
                response['extendedChange'] = response['extendedChange'] * -1
            else:
                arrow = emo.UP_ARROW            
            change = str(response['extendedChange']) + " (" + str(response['extendedChangePercent']) + ")"
            return "{0:<10} {1:>8} {2:<4}".format("Today: ", change, arrow)
        return ""

    def _getOpen(self, response):
        return "{0:<10} {1:<10}".format("Open:", response['open'])
    
    def _getPriceHigh(self, response):
        return "{0:<10} {1:<10}".format("High:", response['high'])

    def _getPriceLow(self, response):
        return "{0:<10} {1:<10}".format("Low:", response['low'])

    def _getVolume(self, response):
        return "{0:<10} {1:<10}".format("Volume:", response['volume'])

    def _getAvgVolume(self, response):
        return "{0:<10} {1:<10}".format("Avg Vol:", response['avg volume'])
    
    def _get52WKHigh(self, response):
        return "{0:<10} {1:<10}".format('52WK High:', response['52weekhigh'])

    def _get52WKLow(self, response):
        return "{0:<10} {1:<10}".format('52WK Low:', response['52weeklow'])

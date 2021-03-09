from plugin import PluginImpl, Keyword
from api.iexcloud import IEXCloud
import util.emoji as emo
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
import logging


class Stockprice(PluginImpl):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)
        self.tgb.dispatcher.add_handler(CallbackQueryHandler(self._callback, pattern="stockprice"))
        self.symbol = ""

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
            # response = IEXCloud().getPrice(context.args[0].upper())
            # print(response)
            self.symbol = context.args[0].upper()
            response = self._getPrice(context.args[0].upper())
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=response, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats())
        except Exception as e:
            print(e)
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)


    def _getPrice(self, symbol):
        try:
            response = IEXCloud().getPrice(symbol)
            return self._getMarkdown(response)
        except Exception as e:
            print("Some error " + e)
            raise e

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <stock ticker>`\n"

    def get_description(self):
        return "Get the current price of a stock"

    def get_category(self):
        return None

    def _callback(self, update, context):
        query = update.callback_query
        query.answer()
        try:
            query.edit_message_text(self._getPrice(query.message.text.split(' ')[0]), parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=self._keyboard_stats())
        except Exception as e:
            logging.error("Unable to update message "  + e)

    def _keyboard_stats(self):
        buttons = [InlineKeyboardButton("Refresh " + emo.REFRESH, callback_data="stockprice")]
        menu = self.build_menu(buttons)
        return InlineKeyboardMarkup(menu, resize_keyboard=True)

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

from plugin import PluginImpl, Keyword
from api.iexcloud import IEXCloud
import util.emoji as emo
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
import logging
from api.stocksg import YahooStocksG

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
            self.symbol = context.args[0].upper()
            response = self._get_stock_data(self.symbol)
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=response, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats())
        except Exception as e:
            print(e)
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)


    def _get_stock_data(self, symbol):
        try:
            stocksg = YahooStocksG()
            stock_data = stocksg.get_data(self.symbol)
            return self._getMarkdown(stock_data)
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
            query.edit_message_text(self._get_stock_data(query.message.text.split(' ')[0]), parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=self._keyboard_stats())
        except Exception as e:
            logging.error("Unable to update message "  + e)

    def _keyboard_stats(self):
        buttons = [InlineKeyboardButton("Refresh " + emo.REFRESH, callback_data="stockprice")]
        menu = self.build_menu(buttons)
        return InlineKeyboardMarkup(menu, resize_keyboard=True)

    def _getMarkdown(self, stock_data):
        output = ""
        try:
            output = "\n" + self._getSymbol(stock_data) + "\n" \
            + self._getPriceRegularHours(stock_data) + "\n"
            
            if stock_data['has_post_market_data']:
                output += self._getPriceAfterHours(stock_data) + "\n"
        
            output += self._getOpen(stock_data) + "\n" \
            + self._getPriceHigh(stock_data) + "\n" \
            + self._getPriceLow(stock_data) + "\n" \
            + self._getVolume(stock_data) + "\n" \
            + self._getAvgVolume(stock_data) + "\n" \
            + self._get52WKHigh(stock_data) + "\n" \
            + self._get52WKLow(stock_data) + "\n"
        except Exception as err:
            print(err)

        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _getSymbol(self, stock_data):
        return "{0:<10} {1:<10}".format(stock_data['symbol'], stock_data['symbol'])

    def _get_change_arrow_emoji(self, stock_data, key):
        arrow = ""
        if "-" in str(stock_data[key]):
            arrow = emo.DOWN_ARROW
        else:
            arrow = emo.UP_ARROW
        return arrow

    def _getPrice(self, stock_data, market_hours):
        price_key = market_hours + '_price'
        price_percent_key = market_hours + '_change_percent'
        arrow = self._get_change_arrow_emoji(stock_data, price_percent_key)
        price_string = stock_data[price_key] \
        + " \(" + stock_data[price_percent_key] + "\)"
        return "{0:<10} {1:>8} {2:<4}".format("Price: ", price_string, arrow)

    def _getPriceRegularHours(self, stock_data):
        return self._getPrice(stock_data, 'regular_market')

    def _getPriceAfterHours(self, stock_data):
        if stock_data['has_post_market_data'] is True:
            return self._getPrice(stock_data, 'post_market').replace("Price", "After-Hours Price")
        return ""

    def _getOpen(self, stock_data):
        return "{0:<10} {1:<10}".format("Open:", stock_data['market_open_price'])
    
    def _getPriceHigh(self, stock_data):
        return "{0:<10} {1:<10}".format("High:", stock_data['regular_market_high'])

    def _getPriceLow(self, stock_data):
        return "{0:<10} {1:<10}".format("Low:", stock_data['regular_market_low'])

    def _getVolume(self, stock_data):
        return "{0:<10} {1:<10}".format("Volume:", stock_data['regular_market_volume'])

    def _getAvgVolume(self, stock_data):
        return "{0:<10} {1:<10}".format("Avg Vol:", stock_data['average_volume'])
    
    def _get52WKHigh(self, stock_data):
        return "{0:<10} {1:<10}".format('52WK High:', stock_data['fifty_two_week_high'])

    def _get52WKLow(self, stock_data):
        return "{0:<10} {1:<10}".format('52WK Low:', stock_data['fifty_two_week_low'])

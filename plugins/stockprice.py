from plugin import PluginImpl, Keyword
import util.emoji as emo
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import escape_markdown
import logging
from api.stocksg import YahooStocksG
from api.count import count

class Stockprice(PluginImpl):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)
        self.tgb.dispatcher.add_handler(CallbackQueryHandler(self._callback))
        
        self.__dispatch_table = {
            'stockprice': self._get_stock_price,
            'company_profile': self._get_company_profile,
            'company_summary': self._get_company_summary
        }

    def get_cmds(self):
        return ["sp"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        count("sp")
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            response = self._get_stock_price(context.args[0].upper())
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=response, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats("stockprice"))
        except Exception as e:
            logging.error(e)
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)

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
            symbol = query.message.text.split()[1]
            query.edit_message_text(self.__dispatch(query.data, symbol), parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup = self._keyboard_stats(query.data))
        except Exception as e:
            logging.error("Unable to update message "  + e)

    def __dispatch(self, request, arg):
        return self.__dispatch_table[request](arg)

    def _keyboard_stats(self, message_type):
        buttons = []
        if message_type == "stockprice":
            buttons = [
                InlineKeyboardButton("Refresh " + emo.REFRESH, callback_data="stockprice"),
                InlineKeyboardButton("Company Profile " + emo.BRIEFCASE, callback_data="company_profile"),
            ]
        elif message_type == "company_profile":
            buttons = [
                InlineKeyboardButton("Stock Price " + emo.UP_ARROW, callback_data="stockprice"),
                InlineKeyboardButton("Company Summary " + emo.NOTEPAD, callback_data="company_summary")
            ]
        elif message_type == "company_summary":
            buttons = [
                InlineKeyboardButton("Stock Price " + emo.UP_ARROW, callback_data="stockprice"),
                InlineKeyboardButton("Company Profile " + emo.BRIEFCASE, callback_data="company_profile")
            ]
        
        menu = self.build_menu(buttons)
        return InlineKeyboardMarkup(menu, resize_keyboard=True)
    
    def _get_stock_data(self, symbol):
        try:
            stocksg = YahooStocksG()
            stock_data = stocksg.get_data(symbol)
            return stock_data
        except Exception as e:
            print("Some error " + e)
            raise e

    def _get_stock_price(self, symbol):
        stock_data = self._get_stock_data(symbol)
        return self._getStockPriceMarkdown(stock_data)

    def _get_company_profile(self, symbol):
        stock_data = self._get_stock_data(symbol)
        return self._get_company_profile_markdown(stock_data)

    def _get_company_summary(self, symbol):
        stock_data = self._get_stock_data(symbol)
        return self._get_company_summary_markdown(stock_data)

    def _get_company_summary_markdown(self, stock_data):
        output = ""
        try:
            output = (str('```')) + "\n" \
                + self._format_text("Symbol: ", self._get_if_exist(stock_data, ['symbol'])) + "\n" \
                + self._format_text("Summary: ", self._get_if_exist(stock_data, ['company_summary'])) \
                + (str('```'))
        except ValueError as err:
            print("Missing company summary.")

        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _get_company_profile_markdown(self, stock_data):
        output = (str('```')) + "\n" \
        + self._format_text("Symbol: ", self._get_if_exist(stock_data, ['symbol'])) + "\n" \
        + self._format_text("Name: ", self._get_if_exist(stock_data, ['company_short_name'])) + "\n" \
        + self._format_text("Sector: ", self._get_if_exist(stock_data, ['sector'])) + "\n" \
        + self._format_text("Employees: ",  self._get_if_exist(stock_data, ['full_time_employees'])) + "\n" \
        + self._format_text("City: ", self._get_if_exist(stock_data, ['city'])) + "\n" \
        + self._format_text("State: ", self._get_if_exist(stock_data, ['state'])) + "\n" \
        + self._format_text("Country: ", self._get_if_exist(stock_data, ['country'])) + "\n" \
        + self._format_text("Website: ", self._get_if_exist(stock_data, ['website'])) + "\n" \
        + (str('```'))
        
        return output.replace(".", "\.").replace("-", "\-").replace("|", "\|")

    def _getStockPriceMarkdown(self, stock_data):
        output = ""
        try:
            output = (str('```')) + "\n" + self._getSymbol(stock_data) + "\n" \
            + "Market Prices" + "\n" \
            + self._getPriceRegularHours(stock_data) + "\n"

            if 'has_post_market_data' in stock_data:
                output += self._getPriceAfterHours(stock_data) + "\n"
    
            output += self._getOpen(stock_data) + "\n" \
            + self._getPriceHigh(stock_data) + "\n" \
            + self._getPriceLow(stock_data) + "\n" \
            + self._getVolume(stock_data) + "\n" \
            + self._getAvgVolume(stock_data) + "\n" \
            + self._get52WKHigh(stock_data) + "\n" \
            + self._get52WKLow(stock_data) + "\n" + (str('```'))
        except Exception as err:
            print(err)

        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _get_if_exist(self, map, keyList):
        obj = map
        for key in keyList:
            if key in obj:
                obj = obj[key]
            else:
                return ""
        return obj

    def _format_text(self, label, text):
        return "{0:<10} {1:<10}".format(label, text)

    def _getSymbol(self, stock_data):
        return "{0:<10} {1:<10}".format("Symbol: ", stock_data['symbol'])

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
        return "{0:>8} {1:<4}".format(price_string, arrow)

    def _getPriceRegularHours(self, stock_data):
        return "{0:<10} {1:<10}".format("Regular: ", self._getPrice(stock_data, 'regular_market'))

    def _getPriceAfterHours(self, stock_data):
        if stock_data['has_post_market_data'] is True:
            return "{0:<10} {1:<10}".format("After: ", self._getPrice(stock_data, 'post_market'))
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

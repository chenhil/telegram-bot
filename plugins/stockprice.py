from plugin import PluginImpl, Keyword
import util.emoji as emo
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from telegram.utils.helpers import escape_markdown
import logging

from datetime import datetime, time
from pytz import timezone

from api.stocksg import YahooStocksG
from api.count import count

# US_MARKET times in seconds
US_EASTERN_TIMEZONE = timezone('US/Eastern')
PRE_MARKET_START = 14400
REGULAR_MARKET_START = 34200
POST_MARKET_START = 57600
MARKET_END = 86400

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
        return ["sp", "s"]

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
        current_time = get_current_time()
        try:
            output = (str('```')) + "\n" + self._getSymbol(stock_data) + "\n\n"
            
            if is_pre_market_hours(current_time):
                output += self._get_pre_market_price_markdown(stock_data) + "\n"
            elif is_post_market_hours(current_time):
                output += self._get_post_market_price_markdown(stock_data) + "\n"
            elif is_market_closed(current_time):
                output += self._get_closed_market_markdown(stock_data) + "\n"
            else:
                output += self._get_regular_market_price_markdown(stock_data) + "\n"

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
    
    def _getSymbol(self, stock_data):
        return "{0:<10} {1:<10}".format("Symbol: ", stock_data['symbol'])

    def _getPrice(self, stock_data, market_hours):
        price_key = market_hours + '_price'
        price_percent_key = market_hours + '_change_percent'
        arrow = self._get_change_arrow_emoji(stock_data, price_percent_key)
        price_string = stock_data[price_key] \
        + " \(" + stock_data[price_percent_key] + "\)"
        return "{0:>8} {1:<4}".format(price_string, arrow)

    def _get_change_arrow_emoji(self, stock_data, key):
        arrow = ""
        if "-" in str(stock_data[key]):
            arrow = emo.DOWN_ARROW
        else:
            arrow = emo.UP_ARROW
        return arrow

    def _get_pre_market_price_markdown(self, stock_data):
        output = "Market Status - Pre-Market {0}\n".format(emo.SUNRISE_CITY)
        
        if stock_data['has_pre_market_data'] == True:
            output += "{0:<10} {1:<10}\n\n".format("Price:", self._getPrice(stock_data, 'pre_market'))

        output += "Yesterday's Prices " + "\n" \
        + "{0:<10} {1:<10}\n".format("After:", self._getPrice(stock_data, 'regular_market')) \
        + "{0:<10} {1:<10}\n".format("Regular:", self._getPrice(stock_data, 'post_market'))
        return output

    def _get_regular_market_price_markdown(self, stock_data):
        output = "Market Status - Regular Hours {0}\n".format(emo.CITY) \
            + "{0:<10} {1:<10}\n".format("Price:", self._getPrice(stock_data, 'regular_market'))

    def _get_post_market_price_markdown(self, stock_data):
        output = "Market Status - After-Hours {0}\n".format(emo.DUSK_CITY)
        if stock_data['has_post_market_data'] == True:
            output += "{0:<10} {1:<10}\n".format("After:", self._getPrice(stock_data, 'post_market')) \
                + "{0:<10} {1:<10}\n".format("Regular:", self._getPrice(stock_data, 'regular_market'))
        return output

    def _get_closed_market_markdown(self, stock_data):
        output = "Market Status - Closed {0}\n".format(emo.NIGHT_CITY) 
        if stock_data['has_post_market_data'] == True:
            output += "{0:<10} {1:<10}\n".format("After:", self._getPrice(stock_data, 'post_market')) \
                + "{0:<10} {1:<10}\n".format("Regular:", self._getPrice(stock_data, 'regular_market'))
        return output

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

def get_current_time():
    current_time = datetime.now(tz=US_EASTERN_TIMEZONE)
    return current_time

def get_day_start_seconds(current_time):
    day_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(day_start.timestamp())

def is_pre_market_hours(current_time):
    day_start = get_day_start_seconds(current_time)
    current_time_seconds = int(current_time.timestamp())
    return is_between_interval(day_start + PRE_MARKET_START, day_start + REGULAR_MARKET_START, current_time_seconds)

def is_post_market_hours(current_time):
    day_start = get_day_start_seconds(current_time)
    current_time_seconds = int(current_time.timestamp())
    return is_between_interval(day_start + POST_MARKET_START, day_start + MARKET_END, current_time_seconds)

# Before pre-market of next day and after current day's close
def is_market_closed(current_time):
    day_start = get_day_start_seconds(current_time)
    current_time_seconds = int(current_time.timestamp())

    # After midnight...
    if current_time_seconds < day_start + PRE_MARKET_START:
        return is_between_interval(day_start, day_start + PRE_MARKET_START, current_time_seconds)
    # Before midnight..
    else:
        return current_time_seconds >= day_start + MARKET_END

# Non-inclusive [ intervalStart , intervalEnd ) interval checking
# If a time to check is not given, this defaults to the current time.
def is_between_interval(interval_begin, interval_end, check_time):
    if interval_begin < interval_end:
        return check_time >= interval_begin and check_time < interval_end
    else: # crosses midnight
        return check_time >= interval_begin or check_time < interval_end
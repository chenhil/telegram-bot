from plugin import PluginImpl, Keyword
from api.coinmarketcap import CoinMarketCap
from api.coingecko import CoinGecko
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from api.count import count
import util.emoji as emo
import logging, traceback 


class Cryptoprice(PluginImpl):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)
        self.tgb.dispatcher.add_handler(CallbackQueryHandler(self._callback, pattern='cryptoprice'))
        self.symbol = ""

    def get_cmds(self):
        return ["p"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        count("p")
        if len(context.args) != 1:
            # update.message.reply_text(
            #     text=f"Usage:\n{self.get_usage()}",
            #     parse_mode=ParseMode.MARKDOWN)
            response = self._getPrice('btc') + "\n\n" + self._getPrice('eth')
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=response, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats())
            return
        try:
            response = self._getPrice(context.args[0])
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=response, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats())
        except Exception as e:
            print(traceback.print_exc())
            return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <symbol>`\n"

    def get_description(self):
        return "Get the current price of a cryto/stock"

    def get_category(self):
        return None

    def _getPrice(self, symbol):
        try:
            coinSymbol = CoinGecko().getCoinList(symbol)
            if coinSymbol is None:
                raise Exception("Invalid crypto symbol")
            responseCMC = CoinMarketCap().getPrice(coinSymbol['symbol'].upper())
            responseGecko = CoinGecko().getPrice(coinSymbol['id'])
            output = (self._getMarkdown(responseCMC)
            + "`via CoinMarketCap`"
            + "\n\n"
            + self._getMarkdown(responseGecko)
            + "`via CoinGecko`")
            return output
        except Exception as e:
            print(e)
            raise e        

    def _callback(self, update, context):
        query = update.callback_query
        query.answer()
        try:
            symbol = query.message.text.split(' ')[0]

            query.edit_message_text(self._getPrice(symbol), parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=self._keyboard_stats())
        except Exception as e:
            logging.error("Unable to update message")

    def _keyboard_stats(self):
        buttons = [InlineKeyboardButton("Refresh " + emo.REFRESH, callback_data="cryptoprice")]
        menu = self.build_menu(buttons)
        return InlineKeyboardMarkup(menu, resize_keyboard=True)

    def _getMarkdown(self, response):
        output = ""
        try:
            output = (str('```')) + "\n" + self._getSymbol(response) + "\n" \
            + self._getPercentChange1h(response) + "\n" \
            + self._getPercentChange24h(response) + "\n" \
            + self._getPercentChange7d(response) + "\n" \
            + self._getPriceLow(response) + "\n" \
            + self._getPriceHigh(response) + "\n" \
            + self._getVolume(response) + "\n" \
            + self._getMarketCap(response) + "\n" \

            if 'allTimeHigh' in response:
                output += self._getAllTimeHigh(response) + "\n"
    
            output +=  (str('```'))
        except Exception as err:
            print(err)
        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _getSymbol(self, response):
        return self._formatRow(response['symbol'], response['price'])

    def _getPercentChange1h(self, response):
        if 'percentChange1h' in response:
            return self._formatRow("1h:", response['percentChange1h'])
        else:
            return ""
        
    
    def _getPercentChange24h(self, response):
        return self._formatRow("24h:", response['percentChange24h'])

    def _getPercentChange7d(self, response):
        return self._formatRow("7d:", response['percentChange7d'])
    
    def _getVolume(self, response):
        return self._formatRow("Vol 24h:", response['volume24'])

    def _getPriceLow(self, response):
        return self._formatRow("24L:", response['priceLow'])
    
    def _getPriceHigh(self, response):
        return self._formatRow("24H:", response['priceHigh'])

    def _getMarketCap(self, response):
        return self._formatRow("Cap:", response['marketCap'])
    
    def _getAllTimeHigh(self, response):
        return self._formatRow("ATH:", response['allTimeHigh'])

    def _formatRow(self, input1, input2):
        return "{0:<10} {1:<10}".format(input1, input2) 

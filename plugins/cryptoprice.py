from plugin import PluginImpl, Keyword
from api.coinmarketcap import CoinMarketCap
from api.coingecko import CoinGecko
from api.uniswap import Uniswap
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
    @PluginImpl.save_data
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:

            response = self._getPrice(context.args[0])
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=response, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats(context.args[0]))
        except Exception as e:
            print(traceback.print_exc())
            return self.handle_error(f"Error. Invalid symbol {context.args[0].upper()} ", update)

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <ticker>`\n"

    def get_description(self):
        return "Get the current price of a cryto/stock"

    def get_category(self):
        return None

    def _getPrice(self, symbol):
        try:
            coinSymbols = CoinGecko().getCoinList(symbol)
            uniswapInfo = Uniswap().getPriceUniswap(symbol.upper())
            if len(coinSymbols) == 0:
                raise Exception("Invalid crypto symbol")
            output = ''
            for coinSymbol in coinSymbols:
                responseGecko = CoinGecko().getPrice(coinSymbol['id'])
                if responseGecko is not None:
                    output += (self._getMarkdown(responseGecko) + "`via CoinGecko`") + "\n\n"
            if uniswapInfo is not None:
                output += (self._getMarkdown(uniswapInfo)
                + "`via Uniswap`" + "\n\n") 
            return output
        except Exception as e:
            print(traceback.print_exc())
            logging.error(e)
            raise e        

    def _callback(self, update, context):
        query = update.callback_query
        query.answer()
        try:
            symbol = update.callback_query.data.split(' ')[1]
            query.edit_message_text(self._getPrice(symbol), parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=self._keyboard_stats(symbol))
        except Exception as e:
            print(traceback.print_exc())
            logging.error(e)
            logging.error("Unable to update message")

    def _keyboard_stats(self, symbol):
        buttons = [InlineKeyboardButton("Refresh " + emo.REFRESH, callback_data="cryptoprice " + symbol)]
        menu = self.build_menu(buttons)
        return InlineKeyboardMarkup(menu, resize_keyboard=True)

    def _getMarkdown(self, response):
        output = ""
        try:
            output = (str('```')) + "\n" + self._getSymbol(response) \
            + self._getPercentChange1h(response) \
            + self._getPercentChange24h(response) \
            + self._getPercentChange7d(response) \
            + self._getPriceLow(response) \
            + self._getPriceHigh(response) \
            + self._getVolume(response) \
            + self._getMarketCap(response) \

            if 'allTimeHigh' in response:
                output += self._getAllTimeHigh(response)
    
            output +=  (str('```'))
        except Exception as err:
            print(traceback.print_exc())
        return output.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|")

    def _getSymbol(self, response):
        return self._formatRow(response['symbol'] + " | " + response['name'], response['price'])

    def _getPercentChange1h(self, response):
        return self._formatRow("1h:", response['percentChange1h']) if 'percentChange1h' in response else ""
        
    def _getPercentChange24h(self, response):
        return self._formatRow("24h:", response['percentChange24h']) if 'percentChange24h' in response else ""

    def _getPercentChange7d(self, response):
        return self._formatRow("7d:", response['percentChange7d']) if 'percentChange7d' in response else ""
    
    def _getVolume(self, response):
        return self._formatRow("Vol 24h:", response['volume24']) if 'volume24' in response else ""

    def _getPriceLow(self, response):
        return self._formatRow("24L:", response['priceLow']) if 'priceLow' in response else ""
    
    def _getPriceHigh(self, response):
        return self._formatRow("24H:", response['priceHigh']) if 'priceHigh' in response else ""

    def _getMarketCap(self, response):
        return self._formatRow("Cap:", response['marketCap']) if 'marketCap' in response else ""
    
    def _getAllTimeHigh(self, response):
        return self._formatRow("ATH:", response['allTimeHigh'])

    def _formatRow(self, input1, input2):
        return "{0:<10} {1:<10}\n".format(input1, input2) 

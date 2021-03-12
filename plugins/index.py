from telegram import ParseMode
from plugin import PluginImpl
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
from api.coingecko import CoinGecko
from uuid import uuid4
import logging
import decimal


class Index(PluginImpl):

    def __init__(self, telegram_bot):
        super().__init__(telegram_bot)
        self.tgb.dispatcher.add_handler(CallbackQueryHandler(self._callback, pattern="^index"))

    def get_cmds(self):
        return ["index"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        # Needs to be moved into a cache
        CoinGecko().getMarketData()

        context.user_data['index'] = 'usd'
        context.user_data['page'] = 0
        context.user_data['timeframe'] = '24h'

        data = self._getMarkdown("usd", 0, "24h")
        update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=data, parse_mode=ParseMode.MARKDOWN_V2, 
            reply_markup=self._keyboard_stats(0))
    
    def get_usage(self):
        return f"`/{self.get_cmds()[0]}`\n"

    def get_description(self):
        return "get market data of all crypto"

    def get_category(self):
        return None

    def _keyboard_stats(self, pageValue):
        header = []
        if pageValue > 0:
            header.append(InlineKeyboardButton("Prev 10", callback_data="index_prev"))

        if pageValue < 9:
            header.append(InlineKeyboardButton("Next 10", callback_data="index_next"))
        buttons = [
            InlineKeyboardButton("BTC", callback_data="index_btc"),
            InlineKeyboardButton("USD", callback_data="index_usd"),
            InlineKeyboardButton("ETH", callback_data="index_eth"),
            InlineKeyboardButton("24H", callback_data="index_24h"),
            InlineKeyboardButton("7d", callback_data="index_7d"),
            InlineKeyboardButton("30d", callback_data="index_30d")
        ]

        menu = self.build_menu(buttons, n_cols = 3, header_buttons=header)
        return InlineKeyboardMarkup(menu, resize_keyboard=True)

    def _callback(self, update, context):
        query = update.callback_query
        query.answer()
        indexValue = context.user_data.get('index', 'Not found')
        pageValue = context.user_data.get('page', 'Not found')
        timeframeValue = context.user_data.get('timeframe', 'Not found')
        if query.data == "index_btc":
            indexValue = 'btc'
            context.user_data['index'] = 'btc'
        elif query.data == 'index_eth':
            indexValue = 'eth'
            context.user_data['index'] = 'eth'
        elif query.data == 'index_usd':
            indexValue = 'usd'
            context.user_data['index'] = 'usd'
        elif query.data == 'index_24h':
            timeframeValue = '24h'
            context.user_data['timeframe'] = '24h'            
        elif query.data == 'index_7d':
            timeframeValue = '7d'
            context.user_data['timeframe'] = '7d'
        elif query.data == 'index_30d':
            timeframeValue = '30d'
            context.user_data['timeframe'] = '30d'
        elif query.data == 'index_next':
            pageValue = pageValue + 1
            context.user_data['page'] = pageValue
        elif query.data == 'index_prev':
            pageValue = pageValue - 1
            context.user_data['page'] = pageValue
        data = self._getMarkdown(indexValue, pageValue, timeframeValue)
        try:
            query.edit_message_text(data, parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=self._keyboard_stats(pageValue))
        except Exception as e:
            logging.error("Unable to update message "  + e)

    def _getMarkdown(self, indexValue, pageValue, timeframeValue):
        output = str('```') + "\n" + "Current Currency: {}".format(indexValue.upper()) + "\n" + self._formatRow("#", "Coin", "Price", timeframeValue+"%") + "\n"
        data = CoinGecko().coinMarketData[indexValue][pageValue] 
        percentChange = 'price_change_percentage_{}_in_currency'.format(timeframeValue)
        count = (10 * pageValue)
        for item in data:
            count = count + 1   
            if indexValue == 'usd':
                price_rounded = "$" + self._float_to_string(item['current_price'], 4)
            else:
                price_rounded = self._float_to_string(item['current_price'])
            output += self._formatRow(count, item['symbol'], price_rounded, str(round(item[percentChange], 2))+"%" ) + "\n"
        output += str('```')
        return output

    def _formatRow(self, *args):
        return '{0:<3}{1:<5}{2:>10}{3:>8}'.format(*args)
        
    def _float_to_string(self, number, precision=8):
        return '{0:.{prec}f}'.format(
            decimal.Context(prec=100).create_decimal(str(number)),
            prec=precision,
        ).rstrip('0').rstrip('.') or '0'
from telegram import ParseMode
from plugin import PluginImpl
from api.coingecko import CoinGecko
from api.cache import Cache
from datetime import datetime
import logging, traceback 
import util.emoji as emo


class Bio(PluginImpl):

    def get_cmds(self):
        return ["bio"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            # coinSymbols = CoinGecko().getCoinList(context.args[0])
            coinlist = Cache.get_coingecko_list()
            symbol = context.args[0]
            output = ''
            for item in coinlist:
                if symbol.upper() == item['name'].upper() or symbol.upper() == item['symbol'].upper():
                    coinData = CoinGecko().getCoinData(item)
                    output += self._getMarkDownForBio(item, coinData) + "\n\n"
    
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=output, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

        except Exception as e:
            logging.error(e)
            logging.error(traceback.print_exc())
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)
    

    def _getMarkDownForBio(self, coinSymbol, coinData):
        output = "<b>" + coinSymbol['id'] + " | " + coinSymbol['symbol'] + "</b>\n\n"
        output += coinData['description']['en']
        for item in coinData['links']['homepage']:
            if item != '':
                output += "\n\n"
                output += emo.LINK +" "+ item        
        if coinData['links']['twitter_screen_name'] != "":
            output += "\n\n"
            output += emo.LINK +" "+ "https://twitter.com/{}".format(coinData['links']['twitter_screen_name'])
        for item in coinData['links']['chat_url']:
            if item != '':
                output += "\n\n"
                output += emo.LINK +" "+ item
        if coinData['links']['telegram_channel_identifier'] != "":
            output += "\n\n"
            output += emo.LINK + " " + "https://t.me/{}".format(coinData['links']['telegram_channel_identifier'])
        # output += "\n\n\n"
        # output += "<b>Exchange</b>"
        # output += "\n"
        # for exchange in coinData['tickers'][:5]:
        #     output += self._formatRow(exchange['market']['name'] +":", coinSymbol['symbol'] + "/" + exchange['target'])
            
        return output

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <crypto>`\n"

    def get_description(self):
        return "Get bio info related to a coin"


    def _formatRow(self, input1, input2):
        return "{0:<10} {1:<10}\n".format(input1, input2) 
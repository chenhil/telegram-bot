from telegram import ParseMode
from plugin import PluginImpl
from api.coinpaprika import CoinPaprika
from datetime import datetime
import util.emoji as emo
import logging, traceback 


class Tweet(PluginImpl):

    def get_cmds(self):
        return ["tw"]

    @PluginImpl.send_typing
    def get_action(self, update, context):
        if len(context.args) != 1:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return
        try:
            tweets = CoinPaprika().getTweets(context.args[0].upper())
            output = "<b>Newest Tweets for " + context.args[0].upper()+ "</b>\n\n"
            # output = self._formatTweet(tweets[0][0])
            for tweet in tweets[:5]:
                output += self._formatTweet(tweet) + "\n\n\n"
            update.message.bot.send_message(chat_id = update.effective_chat.id, 
            text=output, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.print_exc())
            return self.handle_error(f"Error. Invalid symbol {context.args[0]} ", update)
    
    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <stock ticker>`\n"

    def get_description(self):
        return "Get twitter info related to a coin"

    def _formatTweet(self, tweet):
        status = tweet['status'].replace("\n", '')
        date = datetime.fromisoformat(tweet['date'].replace('Z', ''))
        link = "<a href='{}'>{}</a>".format(tweet['status_link'], 'Tweet')
        retweets = emo.REFRESH + " " + str(tweet['retweet_count'])
        hearts = emo.HEART + " " + str(tweet['like_count'])
        time = date.strftime("%B %d %Y %H:%M")
        return status + "\n" + link + "\n" + time + "\n" + hearts + " " +retweets   
    
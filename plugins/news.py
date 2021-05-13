from telegram import ParseMode
from plugin import PluginImpl
from api.cryptopanic import CryptoPanic
from datetime import datetime
import util.emoji as emo
import logging, traceback 
import util.emoji as emo

class News(PluginImpl):

    filters = ["rising", "hot", "bullish", "bearish", "important", "saved", "lol"]

    def get_cmds(self):
        return ["news"]

    @PluginImpl.send_typing
    @PluginImpl.save_data
    def get_action(self, update, context):
        try:
            if len(context.args) == 0:
                data = CryptoPanic().get_posts()
                
                if not data or not data["results"]:
                    update.message.reply_text(
                        text=f"Couldn't retrieve news",
                        parse_mode=ParseMode.MARKDOWN)
                    return

                output = f"<b>{emo.NEWS} Current News</b>\n\n"
                for new in data["results"][:8]:
                    output += self._formatTweet(new)
                update.message.bot.send_message(chat_id = update.effective_chat.id, 
                text=output, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
            else:
                filterText = context.args[0]
                if filterText not in self.filters:
                    update.message.reply_text( text=f"Wrong filter. Choose from: "
                        f"{', '.join(self.filters)}",
                        parse_mode=ParseMode.MARKDOWN)
                    return              

                output = f"<b>{emo.NEWS} Current News for filter: {filterText}</b>\n\n"
                data = CryptoPanic().get_filtered_news(filterText)
                for new in data["results"][:8]:
                    output += self._formatTweet(new)
                update.message.bot.send_message(chat_id = update.effective_chat.id, 
                text=output, parse_mode=ParseMode.HTML, disable_web_page_preview=True)                

        except Exception as e:
            logging.error(e)
            logging.error(traceback.print_exc())
            return self.handle_error(f"Error.", update)
    
    def get_usage(self):
        return f"`/{self.get_cmds()[0]}\n"

    def get_description(self):
        return "Get crypto news"

    def _formatTweet(self, news):
        if news["kind"] == "news":
            msg = ""
            published = news["published_at"]
            domain = news["domain"]
            title = news["title"]
            url = news["url"]

            t = datetime.fromisoformat(published.replace("Z", "+00:00"))
            month = f"0{t.month}" if len(str(t.month)) == 1 else t.month
            day = f"0{t.day}" if len(str(t.day)) == 1 else t.day
            hour = f"0{t.hour}" if len(str(t.hour)) == 1 else t.hour
            minute = f"0{t.minute}" if len(str(t.minute)) == 1 else t.minute

            msg += f'{t.year}-{month}-{day} {hour}:{minute} - {domain}\n' \
                    f'<a href="{url}">{title.strip()}</a>\n\n'
            return msg
from telegram import ParseMode
from plugin import PluginImpl, Keyword
from api.coinstat import Coinstats
from api.count import count
import os
import psycopg2

class Stat(PluginImpl):
    def get_cmds(self):
        return ["stat"]

    @PluginImpl.save_data
    @PluginImpl.send_typing
    def get_action(self, update, context):
        url = 'postgres://whkrhdwpenhhym:598bb25bd018891284d02f939948b0b25a06df4508c251143f98fe1671a12f43@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d5i6go6su3sf1h'
        connection = psycopg2.connect(url,sslmode='require')
        cursor = connection.cursor()
        query = "select command, count from command order by count desc;"
        cursor.execute(query)

        response = ""
        for record in cursor:
            command = record[0]
            commandCount = record[1]

            text = "{} - {}\n".format(command, commandCount)
            response = response + text

        print(response)
        connection.close()

        update.message.bot.send_message(chat_id = update.effective_chat.id,
            text=self._getMarkdown(str(response)), parse_mode=ParseMode.MARKDOWN_V2)

    def _getMarkdown(self, response):
        if response is None:
            return response
        return response.replace(".", "\\.").replace("-", "\\-").replace("|", "\\|").replace("(", "\\(").replace(")", "\\)")

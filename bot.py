import configparser
import os
import uuid
import logging
import importlib
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters
from database import Database


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Bot():

    plugins = list()

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        apiKey = os.getenv('apiKey') if 'apiKey' in os.environ else config['telegram']['apiKey']
        dbKey = os.getenv('DATABASE_URL') if 'DATABASE_URL' in os.environ else config['postgreSQL']['DATABASE_URL']
        try:
            self.updater = Updater(apiKey, use_context=True)
        except Exception as e:
            exit("ERROR: Bot token not valid")

        self.job_queue = self.updater.job_queue
        self.dispatcher = self.updater.dispatcher

        # connect DB
        self.db = Database(dbKey)

        # Load classes in folder 'plugins'
        self._load_plugins()

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()


    def _load_plugins(self):
        for _, _, files in os.walk("./plugins"):
            for file in files:
                if not file.lower().endswith(".py"):
                    continue
                if file.startswith("_"):
                    continue
                self._load_plugin(file)

    def _load_plugin(self, file):
        try:
            module_name = file[:-3]
            module_path = f"plugins.{module_name}"
            module = importlib.import_module(module_path)

            plugin_class = getattr(module, module_name.capitalize())
            plugin_class(self).after_plugin_loaded()
        except Exception as ex:
            msg = f"File '{file}' can't be loaded as a plugin: {ex}"
            logging.warning(msg)

    # def connectDB(self, config):
    #     try:
    #         dbKey = os.getenv('DATABASE_URL') if 'DATABASE_URL' in os.environ else config['postgreSQL']['DATABASE_URL']
    #         connection = psycopg2.connect(dbKey,sslmode='require')
    #         cursor = connection.cursor()
    #         # Print PostgreSQL details
    #         print("PostgreSQL server information")
    #         print(connection.get_dsn_parameters(), "\n")
    #         # Executing a SQL query
    #         cursor.execute("SELECT version();")
    #         # Fetch result
    #         record = cursor.fetchone()
    #         print("You are connected to - ", record, "\n")

    #         ###########TESTING QUERY###############
    #         # print test table
    #         cursor.execute("SELECT * FROM ACCOUNT;")
    #         record = cursor.fetchone()
    #         print(record)

    #     except Exception as e:
    #         print(e)






if __name__ == '__main__':
    bot2 = Bot()

import configparser
import os
import uuid
import logging
import importlib
import re
from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters

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
        try:
            self.updater = Updater(apiKey, use_context=True)
        except Exception as e:
            exit("ERROR: Bot token not valid")

        self.job_queue = self.updater.job_queue
        self.dispatcher = self.updater.dispatcher

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


if __name__ == '__main__':
    bot2 = Bot()
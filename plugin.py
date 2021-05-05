import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, ChatAction

class PluginInterface:

    # List of command strings that trigger the plugin
    def get_cmds(self):
        method = inspect.currentframe().f_code.co_name
        raise NotImplementedError(f"Interface method '{method}' not implemented")

    # Logic that gets executed if command is triggered
    def get_action(self, bot, update, args, inline=False, notify=True, quote=True):
        method = inspect.currentframe().f_code.co_name
        raise NotImplementedError(f"Interface method '{method}' not implemented")

    # How to use the command
    def get_usage(self):
        return None

    # Short description what the command does
    def get_description(self):
        return None

    # Category for command
    def get_category(self):
        return None

    # Does this command support inline mode
    def inline_mode(self):
        return False

    # Execute logic after the plugin is loaded
    def after_plugin_loaded(self):
        return None

    # Execute logic after all plugins are loaded
    def after_plugins_loaded(self):
        return None

class PluginImpl(PluginInterface):

    def __init__(self, telegram_bot):
        super().__init__()
        self.tgb = telegram_bot
        self.add_plugin()

    @classmethod
    def send_typing(cls, func):
        def _send_typing_action(self, update, context):
            if update.message:
                user_id = update.message.chat_id
            elif update.callback_query:
                user_id = update.callback_query.message.chat_id
            else:
                return func(self, update, context)

            try:
                context.bot.send_chat_action(
                    chat_id=user_id,
                    action=ChatAction.TYPING)
            except Exception as ex:
                logging.error(f"{ex} - {update}")

            return func(self, update, context)
        return _send_typing_action

    @classmethod
    def save_data(cls, func):
        def _save_data(self, update, context):
            if update.message:
                fromObj = update.message.from_user
                cmd = update.message.text
                chatObj = update.message.chat
                date = update.message.date
                messageId = update.message.message_id
            else:
                logging.warning(f"Can't save usage - {update}")
                return func(self, update, context)
            # save_data(self, chatId, messageId, firstName, username, date, text)
            self.tgb.db.save_data(messageId, fromObj, chatObj, cmd, date)
            return func(self, update, context)
        return _save_data        

    def add_plugin(self):
        self.tgb.dispatcher.add_handler(
            CommandHandler(
                self.get_cmds(),
                self.get_action,
                pass_args=True))
        self.tgb.plugins.append(self)
        logging.info(f"Plugin '{type(self).__name__}' added")

    def remove_plugin(self):
        for handler in self.tgb.dispatcher.handlers[0]:
            if isinstance(handler, CommandHandler):
                if set(handler.command) == set(self.get_cmds()):
                    self.tgb.dispatcher.handlers[0].remove(handler)
                    break

        self.tgb.plugins.remove(self)
        logging.info(f"Plugin '{type(self).__name__}' removed")

    # Handle exceptions (write to log, reply to Telegram message)
    def handle_error(self, error, update, send_error=True):
        cls_name = f"Class: {type(self).__name__}"
        logging.error(f"{repr(error)} - {error} - {cls_name} - {update}")

        if send_error and update and update.message:
            msg = f"{error}"
            update.message.reply_text(msg)

    # Build button-menu for Telegram
    def build_menu(cls, buttons, n_cols=1, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)

        return menu

# Keywords for messages
class Keyword:
    NOTIFY = "notify"
    PREVIEW = "preview"
    QUOTE = "quote"
    PARSE = "parse"
    INLINE = "inline"
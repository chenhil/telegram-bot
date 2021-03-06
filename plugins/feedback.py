from telegram import ParseMode
from plugin import PluginImpl


class Feedback(PluginImpl):

    def get_cmds(self):
        return ["feedback"]

    @PluginImpl.send_typing
    def get_action(self, update, context):

        if len(context.args) == 0:
            update.message.reply_text(
                text=f"Usage:\n{self.get_usage()}",
                parse_mode=ParseMode.MARKDOWN)
            return

        # user = update.message.from_user
        # if user.username:
        #     name = f"@{user.username}"
        # else:
        #     name = user.first_name

        # feedback = update.message.text.replace(f"/{self.get_cmds()[0]} ", "")



        update.message.reply_text(f"Thanks for letting us know")

    def get_usage(self):
        return f"`/{self.get_cmds()[0]} <your feedback>`\n"

    def get_description(self):
        return "Send us your feedback"

    def get_category(self):
        return None

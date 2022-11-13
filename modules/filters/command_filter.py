from telegram.ext import MessageFilter

class CommandFilter(MessageFilter):

    def filter(self, message) -> bool:
        """Returns true if message starts with the given keyword
        Args:
            message: user message passed by the handler 
        """
        return message.text and message.text.startswith("!dado")
        
from telegram.ext import MessageFilter

class ToniparroCommandFilter(MessageFilter):

    def filter(self, message) -> bool:
        """Returns true if message starts with the given keyword
        Args:
            message: user message passed by the handler 
        """
        return message.text and message.text.startswith("!toniparro")

class DiscordCommandFilter(MessageFilter):

    def filter(self, message) -> bool:
        """Returns true if message starts with the given keyword
        Args:
            message: user message passed by the handler 
        """
        return message.text and message.text.startswith("!discord")

class DiceCommandFilter(MessageFilter):

    def filter(self, message) -> bool:
        """Returns true if message starts with the given keyword
        Args:
            message: user message passed by the handler 
        """
        return message.text and message.text.startswith("!dado")

class ListCommandFilter(MessageFilter):
    
    def filter(self, message) -> bool:
        """Returns true if message starts with !lista
            Args:
                message: user message passed by the handler
        """
        return message.text and message.text.startswith("!lista")
    
class SlotCommandFilter(MessageFilter):
    
    def filter(self, message) -> bool:
        """Returns true if message starts with !lista
            Args:
                message: user message passed by the handler
        """
        return message.text and message.text.startswith("!slot")

class AnonymousCommandFilter(MessageFilter):
    
    def filter(self, message) -> bool:
        """Returns true if message starts with !send_anonymous
            Args:
                message: user message passed by the handler
        """
        return message.text and message.text.startswith("!send_anonymous")
    
class SardaukarCommandFilter(MessageFilter):

    def filter(self, message) -> bool:
        """Returns true if message starts with the given keyword
        Args:
            message: user message passed by the handler 
        """
        return message.text and message.text.startswith("!sardaukar")
    
        
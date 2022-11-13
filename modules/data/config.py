import confuse 

class Config():

    def __init__(self):
        
        self.config = confuse.Configuration('snitch', __name__)
        self.config.set_file('config/application-prod.yaml')
        self.db_host = self.config["mysql"]["host"].get()
        self.db_user = self.config["mysql"]["user"].get()
        self.db_password = self.config["mysql"]["password"].get()
        self.db_database = self.config["mysql"]["db"].get()
        self.bot_token = self.config["bot"]["token"].get()
        self.bot_admin_chat = self.config["bot"]["adminChatId"].get()


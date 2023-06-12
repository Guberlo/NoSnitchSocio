import confuse 

class Config():

    def __init__(self):
        
        self.config = confuse.Configuration('snitch', __name__)
        self.config.set_file('config/application-dev.yaml')
        self.db_host = self.config["mysql"]["host"].get()
        self.db_user = self.config["mysql"]["user"].get()
        self.db_password = self.config["mysql"]["password"].get()
        self.db_database = self.config["mysql"]["db"].get()
        self.db_ca_location = self.config["mysql"]["ca_location"].get()
        self.db_port = self.config["mysql"]["port"].get()
        self.bot_token = self.config["bot"]["token"].get()
        self.bot_admin_chat = self.config["bot"]["adminChatId"].get()
        self.discord_host = self.config["discord"]["host"].get()
        self.discord_port = self.config["discord"]["port"].get()
        self.discord_gif_path = self.config["discord"]["gifPath"].get()
        self.no_link_message = self.config["common"]["noLinkMessage"].get()
        self.error_message = self.config["common"]["errorMessage"].get()
        self.not_found_message = self.config["common"]["notFoundMessage"].get()
        self.scrape_ops_key = self.config["scrapeOps"]["apiKey"].get()



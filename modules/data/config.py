"""Read the bot configuration from the settings.yaml and the reactions.yaml files"""
import os
import re
from typing import Any, Iterable, Literal, Optional
import yaml

SettingsKeys = Literal["debug", "meme", "test", "token", "bot_tag"]
SettingsDebugKeys = Literal["local_log", "reset_on_load"]
SettingsMemeKeys = Literal["channel_group_id", "channel_id", "channel_tag", "comments", "group_id", "n_votes",
                           "remove_after_h", "tag", "report", "report_wait_mins", "replace_anonymous_comments",
                           "delete_anonymous_comments",]
SettingsTestKeys = Literal[Literal["api_hash", "api_id", "session", "bot_tag", "token"], SettingsMemeKeys]
SettingsKeysType = Literal[SettingsKeys, SettingsMemeKeys, SettingsDebugKeys, SettingsTestKeys]

ReactionKeysType = Literal["reactions", "rows"]

class Config():
    """Configurations"""
    SETTINGS_PATH = ("config", "settings.yaml")
    REACTION_PATH = ("data", "yaml", "reactions.yaml")
    __instance: Optional['Config'] = None

    @classmethod
    def reset_settings(cls):
        """Reset the configuration"""
        cls.__instance = None

    @staticmethod
    def __get(config: dict, *keys: str, default: Any = None) -> Any:
        """Get the value of the specified key in the configuration.
        If the key is a tuple, it will return the value of the nested key.
        If the key is not present, it will return the default value.
        Args:
            config: configuration dict to search
            key: key to search
            default: default value to return if the key is not present
        Returns:
            value of the key or default value
        """
        for k in keys:
            if isinstance(config, Iterable) and k in config:
                config = config[k]
            else:
                return default
        return config

    @classmethod
    def __get_instance(cls) -> 'Config':
        """Singleton getter
        Returns:
            instance of the Config class
        """
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def settings_get(cls, *keys: SettingsKeysType, default: Any = None) -> Any:
        """Get the value of the specified key in the configuration.
        If the key is a tuple, it will return the value of the nested key.
        If the key is not present, it will return the default value.
        Args:
            key: key to get
            default: default value to return if the key is not present
        Returns:
            value of the key or default value
        """
        instance = cls.__get_instance()
        return cls.__get(instance.settings, *keys, default=default)    

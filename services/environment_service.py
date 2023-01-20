import os
import sys
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from sqlitedict import SqliteDict


def app_root_path():
    app_path = Path(sys.argv[0]).resolve()
    try:
        if app_path.parent.name == "bin":  # Installed in unixy hierachy
            return app_path.parents[1]
    except IndexError:
        pass
    return app_path.parent


# None will let direnv do its' thing
env_paths = [Path(".env"), app_root_path() / "etc/environment", None]

for env_path in env_paths:
    print("Loading environment from " + str(env_path))
    load_dotenv(dotenv_path=env_path)


class EnvService:
    # To be expanded upon later!
    def __init__(self):
        self.env = {}

    @staticmethod
    def environment_path_with_fallback(env_name, relative_fallback=None):
        directory = os.getenv(env_name)
        if directory is not None:
            return Path(directory).resolve()

        if relative_fallback:
            app_relative = (app_root_path() / relative_fallback).resolve()
            if app_relative.exists():
                return app_relative

        return Path.cwd()

    @staticmethod
    def find_shared_file(file_name):
        share_file_paths = []
        share_dir = os.getenv("SHARE_DIR")
        if share_dir is not None:
            share_file_paths.append(Path(share_dir) / file_name)

        share_file_paths.extend(
            [
                app_root_path() / "share" / file_name,
                app_root_path() / file_name,
                Path(file_name),
            ]
        )

        for share_file_path in share_file_paths:
            if share_file_path.exists():
                return share_file_path.resolve()

        raise ValueError(f"Unable to find shared data file {file_name}")

    @staticmethod
    def get_allowed_guilds():
        # ALLOWED_GUILDS is a comma separated list of guild ids
        # It can also just be one guild ID
        # Read these allowed guilds and return as a list of ints
        try:
            allowed_guilds = os.getenv("ALLOWED_GUILDS")
        except Exception:
            allowed_guilds = None

        if allowed_guilds is None:
            raise ValueError(
                "ALLOWED_GUILDS is not defined properly in the environment file!"
                "Please copy your server's guild ID and put it into ALLOWED_GUILDS in the .env file."
                'For example a line should look like: `ALLOWED_GUILDS="971268468148166697"`'
            )

        allowed_guilds = (
            allowed_guilds.split(",") if "," in allowed_guilds else [allowed_guilds]
        )
        allowed_guilds = [int(guild) for guild in allowed_guilds]
        return allowed_guilds

    @staticmethod
    def get_admin_roles():
        # ADMIN_ROLES is a comma separated list of string roles
        # It can also just be one role
        # Read these allowed roles and return as a list of strings
        try:
            admin_roles = os.getenv("ADMIN_ROLES")
        except Exception:
            admin_roles = None

        if admin_roles is None:
            print(
                "ADMIN_ROLES is not defined properly in the environment file!"
                "Please copy your server's role and put it into ADMIN_ROLES in the .env file."
                'For example a line should look like: `ADMIN_ROLES="Admin"`'
            )
            print("Defaulting to allowing all users to use admin commands...")
            return [None]

        admin_roles = (
            admin_roles.lower().split(",")
            if "," in admin_roles
            else [admin_roles.lower()]
        )
        return admin_roles

    @staticmethod
    def get_dalle_roles():
        # DALLE_ROLES is a comma separated list of string roles
        # It can also just be one role
        # Read these allowed roles and return as a list of strings
        try:
            dalle_roles = os.getenv("DALLE_ROLES")
        except Exception:
            dalle_roles = None

        if dalle_roles is None:
            print(
                "DALLE_ROLES is not defined properly in the environment file!"
                "Please copy your server's role and put it into DALLE_ROLES in the .env file."
                'For example a line should look like: `DALLE_ROLES="Dalle"`'
            )
            print("Defaulting to allowing all users to use Dalle commands...")
            return [None]

        dalle_roles = (
            dalle_roles.lower().split(",")
            if "," in dalle_roles
            else [dalle_roles.lower()]
        )
        return dalle_roles

    @staticmethod
    def get_translator_roles():
        # DALLE_ROLES is a comma separated list of string roles
        # It can also just be one role
        # Read these allowed roles and return as a list of strings
        try:
            translator_roles = os.getenv("TRANSLATOR_ROLES")
        except Exception:
            translator_roles = None

        if translator_roles is None:
            print(
                "TRANSLATOR_ROLES is not defined properly in the environment file!"
                "Please copy your server's role and put it into TRANSLATOR in the .env file."
                'For example a line should look like: `TRANSLATOR="Translate"`'
            )
            print("Defaulting to allowing all users to use Translator commands...")
            return [None]

        translator_roles = (
            translator_roles.lower().split(",")
            if "," in translator_roles
            else [translator_roles.lower()]
        )
        return translator_roles

    @staticmethod
    def get_gpt_roles():
        # GPT_ROLES is a comma separated list of string roles
        # It can also just be one role
        # Read these allowed roles and return as a list of strings
        try:
            gpt_roles = os.getenv("GPT_ROLES")
        except Exception:
            gpt_roles = None

        if gpt_roles is None:
            print(
                "GPT_ROLES is not defined properly in the environment file!"
                "Please copy your server's role and put it into GPT_ROLES in the .env file."
                'For example a line should look like: `GPT_ROLES="Gpt"`'
            )
            print("Defaulting to allowing all users to use GPT commands...")
            return [None]

        gpt_roles = (
            gpt_roles.lower().strip().split(",")
            if "," in gpt_roles
            else [gpt_roles.lower()]
        )
        return gpt_roles

    @staticmethod
    def get_welcome_message():
        # WELCOME_MESSAGE is a default string used to welcome new members to the server if GPT3 is not available.
        # The string can be blank but this is not advised. If a string cannot be found in the .env file, the below string is used.
        # The string is DMd to the new server member as part of an embed.
        try:
            welcome_message = os.getenv("WELCOME_MESSAGE")
        except Exception:
            welcome_message = "Hi there! Welcome to our Discord server!"
        return welcome_message

    @staticmethod
    def get_moderations_alert_channel():
        # MODERATIONS_ALERT_CHANNEL is a channel id where moderation alerts are sent to
        # The string can be blank but this is not advised. If a string cannot be found in the .env file, the below string is used.
        try:
            moderations_alert_channel = os.getenv("MODERATIONS_ALERT_CHANNEL")
        except Exception:
            moderations_alert_channel = None
        return moderations_alert_channel

    @staticmethod
    def get_user_input_api_keys():
        try:
            user_input_api_keys = os.getenv("USER_INPUT_API_KEYS")
            if user_input_api_keys.lower().strip() == "true":
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def get_custom_bot_name():
        try:
            custom_bot_name = os.getenv("CUSTOM_BOT_NAME") + ": "
            return custom_bot_name
        except Exception:
            return "GPTie: "

    @staticmethod
    def get_health_service_enabled():
        try:
            user_input_api_keys = os.getenv("HEALTH_SERVICE_ENABLED")
            if user_input_api_keys.lower().strip() == "true":
                return True
            return False
        except Exception:
            return False

    @staticmethod
    def get_user_key_db_path() -> Union[Path, None]:
        try:
            user_key_db_path = os.getenv("USER_KEY_DB_PATH")
            if user_key_db_path is None:
                return None
            return Path(user_key_db_path)
        except Exception:
            return None

    @staticmethod
    def get_api_db():
        user_input_api_keys = EnvService.get_user_input_api_keys()
        user_key_db = None
        if user_input_api_keys:
            print(
                "This server was configured to enforce user input API keys. Doing the required database setup now"
            )
            # Get user_key_db from environment variable
            user_key_db_path = EnvService.get_user_key_db_path()
            # Check if user_key_db_path is valid
            if not user_key_db_path:
                print(
                    "No user key database path was provided. Defaulting to user_key_db.sqlite"
                )
                user_key_db_path = "user_key_db.sqlite"
            else:
                # append "user_key_db.sqlite" to USER_KEY_DB_PATH if it doesn't already end with .sqlite
                if not user_key_db_path.match("*.sqlite"):
                    # append "user_key_db.sqlite" to USER_KEY_DB_PATH
                    user_key_db_path = user_key_db_path / "user_key_db.sqlite"
            user_key_db = SqliteDict(user_key_db_path)
            print("Retrieved/created the user key database")
            return user_key_db
        return user_key_db

    @staticmethod
    def get_bypass_roles():
        # GPT_ROLES is a comma separated list of string roles
        # It can also just be one role
        # Read these allowed roles and return as a list of strings
        try:
            bypass_roles = os.getenv("CHAT_BYPASS_ROLES")
        except Exception:
            bypass_roles = None

        if bypass_roles is None:
            print(
                "CHAT_BYPASS_ROLES is not defined properly in the environment file!"
                "Please copy your server's role and put it into CHAT_BYPASS_ROLES in the .env file."
                'For example a line should look like: `CHAT_BYPASS_ROLES="bypass"`'
            )
            print("Defaulting to allowing NO ONE to bypass chat moderation")
            return [None]

        bypass_roles = (
            bypass_roles.lower().strip().split(",")
            if "," in bypass_roles
            else [bypass_roles.lower()]
        )
        return bypass_roles

    @staticmethod
    def get_deepl_token():
        try:
            deepl_token = os.getenv("DEEPL_TOKEN")
            return deepl_token
        except Exception:
            return None

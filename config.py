class Config(object):
    # Configuration class for the bot

    # Enable or disable logging
    LOGGER = True

    # Telegram API configuration
    API_ID = 6433468  # Get this value from my.telegram.org/apps
    API_HASH = "7895dfd061f656367ccab30032"

    # Database configuration (PostgreSQL)
    DATABASE_URL = "postgres://rjfkvnmv:IFp9PeY6yDwQMYdSk7uu8wMpX5P7p5QJ@salt.db.elephantsql.com/rjfkvnmv"

    # Event logs chat ID and message dump chat ID
    EVENT_LOGS = -1002128332513

    # Support chat and support ID
    SUPPORT_CHAT = "IOSUPPORTGROUP"
    SUPPORT_ID = -1002128332513

    # Database name
    DB_NAME = "Wolf"

    # Bot token
    TOKEN = "7003923422:AAHYiGyr3HG9OuFzv2lVjpyqtQNKj2IBEXY"  # Get bot token from @BotFather on Telegram

    # Owner's Telegram user ID (Must be an integer)
    MASTER = 5552153244

    # Optional configuration fields
    # List of groups to blacklist
    BL_CHATS = []

    # User IDs of sudo users, dev users, support users, tiger users, and whitelist users
    ASCETIC = []  # Sudo users

    # Toggle features
    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True

    # Modules to load or exclude
    LOAD = []
    NO_LOAD = []

    # Global ban settings
    STRICT_GBAN = True

    # Temporary download directory
    TEMP_DOWNLOAD_DIRECTORY = "./"


class Production(Config):
    # Production configuration (inherits from Config)

    # Enable or disable logging
    LOGGER = True


class Development(Config):
    # Development configuration (inherits from Config)

    # Enable or disable logging
    LOGGER = True

import asyncio
import logging
import sys
import time
import os

from pyrogram import Client
from telegram.ext import Application
from telegram.constants import ParseMode
from config import *

StartTime = time.time()

loop = asyncio.get_event_loop()

# Initialize the logger
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("Logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
# Set the log levels for specific libraries
logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)

# Define the logger for this module
LOGGER = logging.getLogger(__name__)

# Check Python version
if sys.version_info < (3, 6):
    LOGGER.error(
        "You MUST have a Python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

# Check config file
ENV = bool(os.environ.get("ENV", False))

if ENV:
    API_ID = int(os.environ.get("API_ID", None))
    API_HASH = os.environ.get("API_HASH", None)
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    DB_URI = os.environ.get("DATABASE_URL")
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    DB_NAME = os.environ.get("DB_NAME", "Wolf")
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", True))
    SUPPORT_ID = int(os.environ.get("SUPPORT_ID", "-100"))  # Support 
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "IOSUPPORTGROUP")
    TOKEN = os.environ.get("TOKEN", None)

    # Parse the lists of users
    try:
        MASTER = int(os.environ.get("MASTER", None))
    except ValueError:
        raise Exception("Your MASTER env variable is not a valid integer.")
    
    try:
        ASCETIC = set(int(x) for x in os.environ.get("ASCETIC", "").split())
    except ValueError:
        raise Exception("Your sudo list does not contain valid integers.")

else:
    # Use the variables from the config.py file
    from config import Development as Config
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ALLOW_EXCL = Config.ALLOW_EXCL
    DB_URI = Config.DATABASE_URL
    EVENT_LOGS = Config.EVENT_LOGS
    DB_NAME = Config.DB_NAME
    STRICT_GBAN = Config.STRICT_GBAN
    SUPPORT_ID = Config.SUPPORT_ID
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    TOKEN = Config.TOKEN

    # Read and validate integer variables
    try:
        MASTER = int(Config.MASTER)
    except ValueError:
        raise Exception("Your MASTER variable is not a valid integer.")
    
    try:
        ASCETIC = set(int(x) for x in Config.ASCETIC or [])
    except ValueError:
        raise Exception("Your sudo list does not contain valid integers.")

ASCETIC.add(MASTER)

# Application
dispatcher = Application.builder().token(TOKEN).build()
function = dispatcher.add_handler

app = Client("Wolf", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# Alive Message
START_IMG = "https://telegra.ph/file/506b055da5642e1517acc.jpg"

# Booting Message
async def send_booting_message():
    bot = dispatcher.bot

    try:
        await bot.sendMessage(
            chat_id=SUPPORT_ID,
            text="Werewolf is booting up...",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        LOGGER.warning(
            "[ERROR] - Bot isn't able to send a message to the SUPPORT_CHAT!"
        )
        print(e)

loop.run_until_complete(
    asyncio.gather(dispatcher.bot.initialize(), send_booting_message())
)

# Get bot information
print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

# Define the support staff
SUPPORT_STAFF = [int(MASTER)] + list(ASCETIC)
ASCETIC = list(ASCETIC) + [int(MASTER)]
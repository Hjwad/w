import contextlib
import html
import importlib
import json
import re
import time
import traceback

from typing import Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User, Chat, Message
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.error import (
    BadRequest,
    ChatMigrated,
    Forbidden,
    NetworkError,
    TelegramError,
    TimedOut,
)
from telegram.ext import (
    ApplicationHandlerStop,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    CallbackContext,
    MessageHandler,
    filters,
)

from Wolf import (
    MASTER,
    ASCETIC,
    SUPPORT_CHAT,
    SUPPORT_ID,
    BOT_NAME,
    BOT_USERNAME,
    StartTime,
    dispatcher,
    function,
    loop,
)


# Texts
START_TEXT = f"Hey! This is {BOT_NAME}.\n\n"
HELP_TEXT = f"Choose from the list of modules and learn about the commands they have in them.\n\n"

# Images
START_IMG = "https://telegra.ph/file/506b055da5642e1517acc.jpg"

# Buttons
BUTTON = [
    [
        InlineKeyboardButton(text="Recruit Me", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
    
        InlineKeyboardButton(text="Modules", callback_data="wolf_modules"),
    ],
    [
        InlineKeyboardButton(text="Developer", url=f"tg://user?id={MASTER}"),
    ],
]


# Functions
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


async def start(update: Update, context: CallbackContext):
    await update.message.reply_photo(
        photo=START_IMG,
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(BUTTON),
    )

def main():
    function(CommandHandler("start", start))

    print("[INFO]: Bot is now running!")
    dispatcher.run_polling()

if __name__ == "__main__":
    main()
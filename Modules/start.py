from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

import Database.game_sql as sql
import Database.players_sql as player

from Wolf import function
from Wolf.utils.admin import admin_only

# Inline Buttons
JOIN_BUTTON = [
    InlineKeyboardButton(text="Join Game", callback_data=join_game),
]

@admin_only
async def startgame(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message = update.effective_message
    game = sql.create_game_session(user_id)

    if game:
        await message.reply_document(chat_id, document="CgACAgUAAx0Cf_N1MwACKRJmHnO0BMF5Q2Txu4IQwXbL466WhAACqQ0AAvdwAAFUwuthuLSmjIo0BA")
        await message.reply_text(
            text="A new game has been started!",
            reply_markup=InlineKeyboardMarkup(JOIN_BUTTON),
        )
    else:
        await message.reply_text(
            text="A game has already been started"
        )

async def join_game(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat.id

    game_session = sql.get_game_session(chat_id, query.data)
    if game_session:
        player_obj = player.create_player(user_id, query.data)
        if player_obj:
            await query.message.reply_text(
                text=f"You have joined the game {game_session.game_session_id}"
            )
        else:
            await query.message.reply_text(
                text=f"You are already in the game {game_session.game_session_id}"
            )
    else:
        await query.message.reply_text(
            text=f"Game {query.data} does not exist"
        )

function(CommandHandler("startgame", startgame))
function(CallbackQueryHandler(join_game, pattern="^join_game$"))

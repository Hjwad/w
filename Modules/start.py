from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from Database import SESSION
from Database.players_sql import GameSession, Player

from Wolf import dispatcher
from Wolf.utils.admin import admin_only

def create_game_session(chat_id):
    # Function to create a new game session in the database
    session = SESSION()  # Initialize a database session
    try:
        existing_session = session.query(GameSession).filter_by(chat_id=chat_id, is_active=True).first()
        if existing_session:
            return existing_session, False  # Return existing session
        else:
            new_session = GameSession(chat_id=chat_id)
            session.add(new_session)
            session.commit()
            return new_session, True  # Return new session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_players_in_game(chat_id):
    with SESSION() as session:
        game_session = session.query(GameSession).filter_by(chat_id=chat_id).first()
        if game_session:
            return game_session.players
        else:
            return []

@admin_only
def startgame(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    game_session, created = create_game_session(chat_id)
    if created:
        # Send image with inline button
        update.message.reply_photo(photo=open('game_image.jpg', 'rb'),
                                   caption="Click the button below to join the game:",
                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Game", callback_data="join_game")]]))
        update.message.reply_text("The game session has started!")
    else:
        update.message.reply_text("A game session is already in progress.")

def list_players(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    players = get_players_in_game(chat_id)
    if players:
        player_list = "\n".join([f"- {player.username}" for player in players])
        update.message.reply_text("Players in the game:\n" + player_list)
    else:
        update.message.reply_text("No players have joined the game yet.")

def join_game(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    with SESSION() as session:
        game_session = session.query(GameSession).filter_by(chat_id=chat_id).first()
        if game_session:
            # Check if the player already exists in the game session
            existing_player = session.query(Player).filter_by(game_session_id=game_session.id, user_id=user_id).first()
            if not existing_player:
                new_player = Player(user_id=user_id, game_session_id=game_session.id)
                session.add(new_player)
                session.commit()
                query.answer("You have joined the game!")
            else:
                query.answer("You are already in the game!")
        else:
            query.answer("No game session found.")

# Register the command handler
startgame_handler = CommandHandler("startgame", startgame)
dispatcher.add_handler(startgame_handler)

# Register the callback query handler for joining the game
dispatcher.add_handler(CallbackQueryHandler(join_game, pattern="join_game"))

# Example command to list players in the game
list_players_handler = CommandHandler("listplayers", list_players)
dispatcher.add_handler(list_players_handler)

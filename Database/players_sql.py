from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from Database import BASE, SESSION

class GameSession(BASE):
    __tablename__ = 'game_sessions'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))

    players = relationship("Player", back_populates="game_session")

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def __repr__(self):
        return f"<GameSession(id={self.id}, chat_id={self.chat_id})>"
    
class Player(BASE):
    __tablename__ = 'players'
    user_id = Column(Integer, primary_key=True)
    # Relationship to GameSession table
    session_user_id = Column(Integer, ForeignKey('game_sessions.user_id'))
    session = relationship('GameSession', back_populates='players')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<Player(user_id={self.user_id})>"

    def to_dict(self):
        return {"user_id": self.user_id}


def add_player(username):
    # Create a new player object
    new_player = Player(username)

    # Create a session
    session = SESSION()

    try:
        # Add the player to the session
        session.add(new_player)

        # Commit the session to save the changes to the database
        session.commit()
        print("Player created successfully!")
    except Exception as e:
        # Rollback the session if an error occurs
        session.rollback()
        print("Failed to create player:", e)
    finally:
        # Close the session
        session.close()

def get_player(user_id):
    try:
        return SESSION.query(Player).filter_by(user_id=user_id).first()
    finally:
        SESSION.close()


def delete_player(player_user_id):
    try:
        player = SESSION.query(Player).filter_by(user_id=player_user_id).first()
        if player:
            SESSION.delete(player)
            SESSION.commit()
            print("Player deleted successfully!")
        else:
            print("Player not found!")
    except Exception as e:
        print("Failed to delete player:", e)
    finally:
        SESSION.close()

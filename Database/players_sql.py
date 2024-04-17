import threading
from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship
from Database import BASE, SESSION

INSERTION_LOCK = threading.RLock()

class Player(BASE):
    __tablename__ = "players"
    user_id = Column(BigInteger, primary_key=True)
    chat_id = Column(String(14), ForeignKey("game_sessions.chat_id"), primary_key=True)
    user = relationship("User", back_populates="players")
    game_session = relationship("GameSession", back_populates="players")

    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = chat_id

    def __repr__(self):
        return f"<Player user_id={self.user_id} chat_id={self.chat_id}>"

def create_player(user_id, chat_id):
    with INSERTION_LOCK:
        session = SESSION()
        try:
            new_player = Player(user_id=user_id, chat_id=chat_id)
            session.add(new_player)
            session.commit()
            return new_player
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

def get_player(user_id, chat_id):
    with INSERTION_LOCK:
        session = SESSION()
        try:
            return session.query(Player).filter_by(user_id=user_id, chat_id=chat_id).first()
        finally:
            session.close()

def del_player(user_id, chat_id):
    with INSERTION_LOCK:
        session = SESSION()
        try:
            player = session.query(Player).filter_by(user_id=user_id, chat_id=chat_id).first()
            if player:
                session.delete(player)
                session.commit()
                return True
            else:
                return False
        finally:
            session.close()

BASE.metadata.create_all(SESSION.bind)

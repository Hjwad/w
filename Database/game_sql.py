import threading
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Database import BASE, SESSION

INSERTION_LOCK = threading.RLock()

class GameSession(BASE):
    __tablename__ = "game_sessions"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, ForeignKey("chats.chat_id"))
    is_active = Column(Boolean, default=True)
    players = relationship("Player", back_populates="game_session")

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.is_active = True

    def __repr__(self):
        return f"<GameSession chat_id={self.chat_id} is_active={self.is_active}>"

def create_game_session(chat_id):
    with INSERTION_LOCK:
        session = SESSION()
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

def get_game_session(chat_id, game_session_id):
    with INSERTION_LOCK:
        session = SESSION()
        try:
            return session.query(GameSession).filter_by(chat_id=chat_id, game_session_id=game_session_id, is_active=True).first()
        finally:
            session.close()

def del_game_session(chat_id):
    with INSERTION_LOCK:
        session = SESSION()
        try:
            game_session = session.query(GameSession).filter_by(chat_id=chat_id, is_active=True).first()
            if game_session:
                game_session.is_active = False
                session.commit()
                return True
            else:
                return False
        finally:
            session.close()

BASE.metadata.create_all(SESSION.bind)

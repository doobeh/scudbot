from database import Base, ASCII
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

class User(Base):
    __tablename__ = 'user'
    nick = Column(String(100), primary_key=True)
    messages = relationship("Message", backref="user", lazy="dynamic")

    def __init__(self, nick):
        self.nick = nick

    def __repr__(self):
        return "%s \n%s" % (self.nick, "\n".join(str(x) for x in self.messages))
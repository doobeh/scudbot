from database import Base, ASCII
from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref


class Channel(Base):
    __tablename__ = 'channel'
    name = Column(ASCII(100), primary_key=True)
    messages = relationship("Message", backref="channel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
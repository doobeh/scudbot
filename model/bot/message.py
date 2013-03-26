from database import Base, ASCII
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime


# TODO add urls to the message
class Message(Base):
    __tablename__ = 'message'
    mid = Column(Integer, primary_key=True)
    network_name = Column(String(100), ForeignKey('network.name'))
    user_id = Column(String(100), ForeignKey('user.nick'))
    channel_id = Column(String(100), ForeignKey('channel.name'))
    message = Column(Text())
    is_action = Column(Boolean())
    urls = relationship("Url", backref="message", lazy="dynamic")
    date_created = Column(DateTime, default=datetime.now())
    private = Column(Boolean, default=False)

    def __init__(self, user, network, channel, message ,is_action=False):
        self.user = user
        self.message = message
        self.network = network
        self.channel = channel
        self.is_action = is_action
        self.date_created = datetime.now()

    def __repr__(self):
        return "[%s@%s] %d:%s" % (self.date_created, self.channel.name, self.mid, self.message)

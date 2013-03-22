from database import Base, ASCII
from sqlalchemy import Column, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

#Bot to Channel association because one bot can have many 
#channels and a channel can be looked over by many bots.
bot_to_channel = Table('bot_channel', Base.metadata,
                       Column('bot_nick', ASCII(100), ForeignKey('bot.nick')),
                       Column('channel_id', ASCII(100), ForeignKey('channel.name')))


class Bot(Base):
    __tablename__ = 'bot'
    nick = Column(ASCII(100), primary_key=True)
    active = Column(Boolean(), default=True)

    #Network Server Relationship
    network_name = Column(String(100), ForeignKey('network.name'), primary_key=True)
    network = relationship("Network", lazy="joined")

    #Channel Relationship
    channels = relationship("Channel", secondary=bot_to_channel, backref="bots", lazy="joined")

    def __init__(self, nick, network_name):
        self.nick = nick
        self.network_name = network_name

    def __repr__(self):
        return '%s on %s' % (self.nick, self.network)


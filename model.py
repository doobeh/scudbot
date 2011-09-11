from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship, backref
from database import Base
from datetime import datetime
from math import ceil

class ASCII(TypeDecorator):
    '''Prefixes Unicode values with "PREFIX:" on the way in and
    strips it off on the way out.
    '''
    impl = String

    def process_result_value(self, value, dialect):
        if value is not None:
            return str(value)
        return value

class Network(Base):
    __tablename__ = 'network'
    id = Column(Integer, primary_key=True)
    server = Column(String(100))
    port = Column(Integer())
    network_channels = relationship("NetworkChannel", backref="network", lazy="dynamic")
    
    def __init__(self,server,port=6667):
        self.port = port
        self.server = server
        
    def __repr__(self):
        return '<%s:%s>' % (self.server,self.port)
    

class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(ASCII(100))

    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return '<Channel: %s>' % (self.name,)
    
class Bot(Base):
    __tablename__ = 'bot'
    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, ForeignKey('network.id'))
    network = relationship("Network", lazy="joined")
    network_channels = relationship("NetworkChannel", backref="bot", lazy="joined", collection_class=set)
    nick = Column(ASCII(100))
    active = Column(Boolean(), default=True)
    
    def __init__(self,nick,network):
        self.nick = nick
        self.network = network
        
    def __repr__(self):
        return '<Bot %s on %s>' % (self.nick,self.network)

class NetworkChannel(Base):
    __tablename__ = 'networkchannel'
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey('bot.id'))

    network_id = Column(Integer, ForeignKey('network.id'))
    channel = relationship("Channel")
    channel_id = Column(Integer, ForeignKey('channel.id'))
    messages = relationship("Message", backref="network_channel", lazy="dynamic")
    active = Column(Boolean())
    password = Column(String())
    notes = Column(Text())
    
    def __init__(self,channel,network,password=None,active=True):
        self.channel = channel
        self.network = network
        self.password = password
    
    def __repr__(self):
        return '<%s on %s>' % (self.channel.name, self.network)
    

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nick = Column(String(100))
    messages = relationship("Message", backref="user", lazy="dynamic")
     
    def __init__(self,nick):
        self.nick = nick
        
    def __repr__(self):
        return self.nick
    
class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    network_channel_id = Column(Integer, ForeignKey(NetworkChannel.id))
    user_id = Column(Integer, ForeignKey(User.id))
    message = Column(Text())
    urls = relationship("Url", backref="message", lazy="dynamic")
    date_created = Column(DateTime, default=datetime.now())

    def __init__(self,user,network_channel,message):
        self.user = user
        self.message = message
        self.network_channel = network_channel
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "%s : %s" % (self.user, self.message,)
    
class Url(Base):
    ''' Logs Links '''
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    title = Column(Text)
    page_type = Column(Text)
    link_type = Column(Text)
    file_type = Column(Text)
    img_cached = Column(Boolean)
    img_thumb  = Column(Text)
    message_id = Column(Integer, ForeignKey(Message.id))
    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self, url):
        self.url = url
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "<URL: %s>" % (self.url)    
    


    


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    user = Column(String(100))
    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self, user):
        self.user = user
        self.date_created = datetime.now()
    
    def __repr__(self):
        return "<User: %s>" % (self.user,)


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

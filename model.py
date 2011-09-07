from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from database import Base
from datetime import datetime
from math import ceil


class Network(Base):
    ''' All the networks available '''
    __tablename__ = 'network'
    id = Column(Integer, primary_key=True)
    server = Column(String(100))
    port = Column(Integer())
    bot = relationship("Bot", uselist=False, backref="network")
    
    def __init__(self,server,port):
        self.port = port
        self.server = server
        
    def __repr__(self):
        return '<%s:%s>' % (self.server,self.port)


class Bot(Base):
    ''' What bots will need firing '''
    __tablename__ = 'bot'
    id = Column(Integer, primary_key=True)
    network_id = Column(Integer, ForeignKey(Network.id))
    nick = Column(String(100))
    botchannels = relationship('BotChannel',backref='bot',lazy='dynamic')
    
    def __init__(self,nick):
        self.nick = nick
        
    def __repr__(self):
        return '<Bot %s>' % (self.nick,)


class Channel(Base):
    ''' Channels to be watched '''
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    password = Column(String(100))
    notes = Column(Text())
    server = Column(String(100))
    botchannels = relationship('BotChannel',backref='channel',lazy='dynamic')
    
    def __init__(self,name,password=None,server="uk.quakenet.org"):
        self.name = name
        self.password = password
        self.server = server
    
    def __repr__(self):
        return '<%s on %s>' % (self.name, self.server)
    
    
class BotChannel(Base):
    ''' Channels controlled by each bot '''
    __tablename__ = 'botchannel'
    id = Column(Integer, primary_key=True)
    bot_id = Column(Integer, ForeignKey(Bot.id))
    channel_id = Column(Integer, ForeignKey(Channel.id))
    active = Column(Boolean())
    messages = relationship('Message',backref='botchannel',lazy='dynamic')
    
    def __init__(self,bot,channel,active=True):
        self.channel = channel
        self.bot = bot
        self.active = active
        
    def __repr__(self):
        return '<%s : %s : %s>' % (self.bot.nick, self.bot.network, self.channel)
        
    
class User(Base):
    ''' IRC Users '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nick = Column(String(100))
    messages = relationship('Message',backref='user',lazy='dynamic')
    
    def __init__(self,nick):
        self.nick = nick
        
    def __repr__(self):
        return self.nick
    
    
class Message(Base):
    ''' Logs all IRC Chatter '''
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    botchannel_id = Column(Integer, ForeignKey(BotChannel.id))
    urls = relationship('Url',backref='message',lazy='dynamic')
    user_id = Column(Integer, ForeignKey(User.id))
        
    def __init__(self,user,botchannel,message):
        self.user = user
        self.message = message
        self.botchannel = botchannel
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "%s : %s" % (self.user, self.message,)


class Url(Base):
    ''' Logs Links '''
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    msg = Column(Text)
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

    @property
    def name(self):
        idx = self.nick.find("!")
        if idx == -1:
            return self.nick
        return self.nick[:idx]
    
    
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

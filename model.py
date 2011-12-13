from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship, backref
from flaskext.login import UserMixin
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
    name = Column(String(100), primary_key=True)
    servers = relationship("Server", backref="network", lazy="dynamic")
    
    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return '%s' % (self.name)

class Server(Base):
    __tablename__ = 'server'
    network_name = Column(String(100), ForeignKey('network.name'))
    address = Column(String(100), primary_key=True)
    port = Column(Integer())
    isSSL = Column(Boolean(), default=False)
    
    
    def __init__(self,network_name,address,port=6667,isSSL=False):
        self.network_name = network_name
        self.port = 6667 if port == None else port
        self.address = address
        self.isSSL = isSSL
        
    def __repr__(self):
        if(self.isSSL):
            return '%s: SSL %s:%d' % (self.network_name, self.address,self.port)
        else:
            return '%s: TCP %s:%d' % (self.network_name, self.address,self.port)

class Channel(Base):
    __tablename__ = 'channel'
    name = Column(ASCII(100), primary_key=True)

    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return self.name

#Bot to Channel association because one bot can have many 
#channels and a channel can be looked over by many bots.
bot_to_channel = Table('bot_channel', Base.metadata,
                                Column('bot_nick', ASCII(100), ForeignKey('bot.nick')),
                                Column('channel_id', ASCII(100), ForeignKey('channel.name'))
                                )    
class Bot(Base):
    __tablename__ = 'bot'
    nick = Column(ASCII(100), primary_key=True)
    active = Column(Boolean(), default=True)
    
    #Network Server Relationship
    network_name = Column(String(100), ForeignKey('network.name'), primary_key=True)
    network = relationship("Network", lazy="joined")
    
    #Channel Relationship
    channels = relationship("Channel", secondary=bot_to_channel, backref="bots", lazy="joined", collection_class=set)
    
    def __init__(self,nick,network_name):
        self.nick = nick
        self.network_name = network_name
        
    def __repr__(self):
        return '%s on %s' % (self.nick,self.network)

'''
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
    is_action = Column(Boolean())
    urls = relationship("Url", backref="message", lazy="dynamic")
    date_created = Column(DateTime, default=datetime.now())
    private = Column(Boolean, default=False)

    def __init__(self,user,network_channel,message,is_action=False):
        self.user = user
        self.message = message
        self.network_channel = network_channel
        self.is_action = is_action
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "%s" % (self.message)
'''
def check_existing(context):
    ''' Checks database to see if url link has been mentioned before.

        When a Url object is created, this function checks the existing
        database to see if the link has been mentioned before, if it
        has, it returns the 'original' Url id, which is stored against
        the new Url.
        
    '''

    item = Url.query.filter_by(url=context.current_parameters['url']).filter(Url.original_id == None).first()
    if item:
        return item.id
    return None
'''
class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    title = Column(Text)
    page_type = Column(Text)
    link_type = Column(Text)
    file_type = Column(Text)
    img_cached = Column(Text)
    img_thumb  = Column(Text)
    message_id = Column(Integer, ForeignKey(Message.id))
    date_created = Column(DateTime, default=datetime.now())
    original_id = Column(Integer, ForeignKey("url.id"), default=check_existing)

    def __init__(self, url):
        self.url = url
        self.date_created = datetime.now()

    def __repr__(self):
        return "<URL: %s>" % (self.url)

    @property
    def is_private(self):
        return self.message.private
    
    @property
    def conversation(self):
        m = self.message_id
        nc = self.message.network_channel
        before = Message.query.filter_by(network_channel = nc).filter(Message.id < self.message_id).order_by(Message.id.desc()).limit(2)
        after = Message.query.filter_by(network_channel = nc).filter(Message.id > self.message_id).order_by(Message.id.asc()).limit(2)
        return list(before) + [self.message] + list(after)
'''
class Admin(Base, UserMixin):
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

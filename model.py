from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from database import Base
from datetime import datetime
from math import ceil



class Bot(Base):
    ''' Allocates where the bots live'''
    __tablename__ = 'bot'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    server = Column(String(100))
    channels = relationship('Channel',backref='bot',lazy='dynamic')
    
    def __init__(self,name,server):
        self.name = name
        self.server = server
        
    def __repr__(self):
        return '<%s : %s>' % (self.name, self.server,)
    


class Channel(Base):
    ''' Channels to be watched '''
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    password = Column(String(100))
    notes = Column(Text())
    server = Column(String(100))
    bot_id = Column(Integer, ForeignKey(Bot.id))
    messages = relationship('Message',backref='channel',lazy='dynamic')
    
    def __init__(self,name,password=None,server="uk.quakenet.org"):
        self.name = name
        self.password = password
        self.server = server
    
    def __repr__(self):
        return '<%s on %s>' % (self.name, self.server)
    
    
    
class Message(Base):
    ''' Logs all IRC Chatter '''
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user = Column(String(200))
    #channel = Column(String(200))
    message = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    channel_id = Column(Integer, ForeignKey(Channel.id))
    urls = relationship('Url',backref='message',lazy='dynamic')
    user_id = Column(Integer, ForeignKey(User.id))
    
    @property
    def nick(self):
        return self.user.split("!")[0]
    
    def __init__(self,user,channel,message):
        self.user = user
        self.message = message
        self.channel = channel
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "%s : %s" % (self.user, self.message,)

class User(Base):
    ''' IRC Users '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    nick = Column(String(100))
    messages = relationship('Message',backref='user',lazy='dynamic')

class Url(Base):
    ''' Logs Links '''
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(Text)
    msg = Column(Text)
    nick = Column(Text)
    channel = Column(Text)
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

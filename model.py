from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user = Column(String(200))
    nick = Column(String(100))
    channel = Column(String(200))
    message = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self,user,channel,message):
        self.user = user
        self.message = message
        self.channel = channel
        self.nick = user.split("!")[0]
        
    def __repr__(self):
        return "%s : %s" % (self.user, self.message,)

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    user = Column(String(100))
    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self, user):
        self.user = user
    
    def __repr__(self):
        return "<User: %s>" % (self.user,)
class Url(Base):
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

    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self, url):
        self.url = url
        
    def __repr__(self):
        return "<URL: %s>" % (self.url)

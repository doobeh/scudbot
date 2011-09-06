from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base
from datetime import datetime
from math import ceil

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
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "%s : %s" % (self.user, self.message,)

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
        self.date_created = datetime.now()
        
    def __repr__(self):
        return "<URL: %s>" % (self.url)

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

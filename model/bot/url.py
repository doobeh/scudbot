from database import Base, ASCII
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime


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


#TODO make work
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
    message_id = Column(Integer, ForeignKey("message.mid"))
    date_created = Column(DateTime, default=datetime.now())
    original_id = Column(Integer, ForeignKey("url.id"), default=check_existing)

    def __init__(self, message_id, url):
        self.message_id = message_id
        self.url = url
        self.date_created = datetime.now()

    def __repr__(self):
        return "URL: %s" % self.url

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
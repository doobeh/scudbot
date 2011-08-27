from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from datetime import datetime

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user = Column(String(100))
    channel = Column(String(200))
    message = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self,user,channel,message):
        self.user = user
        self.message = message
        self.channel = channel
        
    def __repr__(self):
        return "%s : %s" % (user, message,)
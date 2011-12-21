from database import Base, ASCII
from sqlalchemy import Column

class Channel(Base):
    __tablename__ = 'channel'
    name = Column(ASCII(100), primary_key=True)

    def __init__(self,name):
        self.name = name
        
    def __repr__(self):
        return self.name
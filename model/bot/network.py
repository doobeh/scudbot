from database import Base, ASCII
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref

class Network(Base):
    __tablename__ = 'network'
    name = Column(String(100), primary_key=True)
    servers = relationship("Server", backref="network", lazy="dynamic")

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '%s' % (self.name)
from database import Base, ASCII
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

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
        
    def __str__(self):
        if(self.isSSL):
            return '%s: SSL %s:%d' % (self.network_name, self.address,self.port)
        else:
            return '%s: TCP %s:%d' % (self.network_name, self.address,self.port)

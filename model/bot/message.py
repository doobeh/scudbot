'''
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
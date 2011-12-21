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
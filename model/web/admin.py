'''
class Admin(Base, UserMixin):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    user = Column(String(100))
    date_created = Column(DateTime, default=datetime.now())
    
    def __init__(self, user):
        self.user = user
        self.date_created = datetime.now()
    
    def __repr__(self):
        return "<User: %s>" % (self.user,)
'''
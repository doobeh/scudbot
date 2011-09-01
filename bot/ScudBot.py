from twisted.words.protocols import irc
from twisted.internet import protocol
from database import db_session
from model import Message, Admin, Url
import re


URL_PATTERN = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
#Regex used previously, will probably use again for capture groups
#prog = re.compile("(?P<link>(?:(?P<ltype>[a-z0-9]{2,15})\:\/\/)?(?:(?P<uname>[-_\w]+)\:?\w*@)?(?:(?P<domain>[\.\-_\w]*\.(?P<ptld>[a-z]{2,}))|(?P<ip>(?:(?:[01]?[0-9]{1,2}|2(?:[0-4][0-9]|5[0-5]))\.){3}(?:[01]?[0-9]{1,2}|2(?:[0-4][0-9]|5[0-5]))))(?:\:(?P<port>\d+))?\/?(?P<pathres>[\w\#\/\Q~:;,.?+=&%@!-\E]+)?)",re.I)
class ScudBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)
        print URL_PATTERN

    def privmsg(self, user, channel, msg):
        
        # Bot is talking to himself?
        if not user:
            return
        
        # Run a command 
        if msg.startswith('!%s' % self.nickname):
            u = Admin.query.filter_by(user=user).first()
            if u:
                print "user %s sent command %s" % (user, msg,)
            else:
                print "user %s not authed for command %s" % (user, msg,)
        
        # Check and log URLS:
        urls = re.findall(URL_PATTERN,msg)
        for url in urls:
            db_session.add(Url(url[0]))
        db_session.commit()
        
        # Log all messages
        m = Message(user, channel, msg)
        db_session.add(m)
        db_session.commit()

class ScudBotFactory(protocol.ClientFactory):
    protocol = ScudBot

    def __init__(self, channel, nickname='ScudBot'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

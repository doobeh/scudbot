from twisted.words.protocols import irc
from twisted.internet import protocol
from database import db_session
from model import Message

class ScudBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
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
from twisted.words.protocols import irc
from twisted.internet import protocol
from database import db_session
from model import Message, Admin
import re
from urlParser import parse


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
        print "Checking message: %s " % (msg)
        print parse(user, channel, msg)
        print "Message Checked"
        
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

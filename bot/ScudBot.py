from twisted.words.protocols import irc
from twisted.internet import protocol
from database import db_session
from model import *
import re
from urlParser import parse


class ScudBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.bot.nick
    nickname = property(_get_nickname)

    def signedOn(self):
        print "Signed on as %s." % (self.factory.bot.nick,)
        for netChan in self.factory.bot.network_channels:
            chan = netChan.channel.name
            print "Joining %s" % (chan)
            if isinstance(chan, unicode):
                print "Channel is Unicode"
            self.join(chan)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        
        # Bot is talking to himself?
        if not user:
            return
        print "%s\n%s-%s: %s" % (self.factory.bot.network.server, user, channel, msg)

        # Does the user exist?
        u = User.query.filter_by(nick=user).first()
        if u is None:
            u = User(user)
            db_session.add(u)
            db_session.commit()
            print "Added User :%s" % (u,)
        else:
            print "Found User :%s" % (u,)

        # Grab the NetworkChannel
        net_channel = [nc for nc in self.factory.bot.network_channels if nc.channel.name == channel[1::]][0]
        print "Network Channel for Message is %s" % (net_channel,)

        # Add the message
        m = Message(u,net_channel,msg)
        db_session.add(m)
        print "Added message %s" % (m,)

        parse(m)

        # Commit the data
        db_session.commit()



        
class ScudBotFactory(protocol.ClientFactory):
    protocol = ScudBot

    def __init__(self, bot):
        self.bot = bot

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)

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
        for netChan in self.factory.bot.network_channels:
            if(channel == netChan.channel.name):
                print "Joined %s." % (channel,)
                return
        self.leave(channel)

    def process_message(self,user,channel,msg,is_action=False):
        # Drop the hostname part of username:
        user = user.split('!')[0]

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
        net_channel = [nc for nc in self.factory.bot.network_channels if nc.channel.name == channel][0]
        print "Network Channel for Message is %s" % (net_channel,)

        # return the message
        message = Message(u,net_channel,msg,is_action)
        if "[wip]" in message.message:
            message.private = True
        return message

    def privmsg(self, user, channel, msg):
        # Bot is talking to himself?
        if not user:
            return
        print "Server: %s\nUser:%s\nChannel:%s\n%s" % (self.factory.bot.network.server, user, channel, msg)
        if channel == self.nickname or channel == '*':
            return

        m = self.process_message(user, channel, msg)
        db_session.add(m)
        print "Added message %s" % (m,)

        parse(m)

        # Commit the data
        db_session.commit()

    def action(self, user, channel, msg):
        # Bot is talking to himself?
        if not user:
            return
        print "%s\n%s-%s: %s" % (self.factory.bot.network.server, user, channel, msg)
        if channel == self.nickname or channel == '*':
            return

        m = self.process_message(user, channel, msg, True)
        db_session.add(m)
        print "Added action %s %s" % (m,m.is_action)
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

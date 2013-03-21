from twisted.internet import ssl, reactor
from bot.ScudBot import ScudBotFactory
from model import Bot

if __name__ == "__main__":
    for bot in Bot.query.all():
        print "[%s] Trying to connect to network %s" % (bot.nick, bot.network.name)
        if(len(bot.network.servers) <= 0):
            print "[%s] Unable to connect to network %s with no servers." % (bot.nick, bot.network.name)
            continue
        else:
            print "[%s] Connecting to %s:%s" % (bot.nick, bot.network.server, bot.network.port)
            botObj = ScudBotFactory(bot)
            if(bot.network.server.isSSL):
                reactor.connectSSL(bot.network.server, bot.network.port, botObj, ssl.ClientContextFactory())
            else:
                reactor.connectTCP(bot.network.server, bot.network.port, botObj)
            reactor.run()

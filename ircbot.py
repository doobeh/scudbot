from twisted.internet import reactor
from bot.ScudBot import ScudBotFactory
from model import Bot

if __name__ == "__main__":
    bot = Bot.query.first()
    print "Connecting to %s:%s" % (bot.network.server, bot.network.port)
    botObj = ScudBotFactory(bot)
    reactor.connectTCP(bot.network.server, bot.network.port,botObj)
    reactor.run()

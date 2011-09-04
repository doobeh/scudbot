from twisted.internet import reactor
from bot.ScudBot import ScudBotFactory

if __name__ == "__main__":
    chan = "fortress.uk.scud"
    reactor.connectTCP('uk.quakenet.org', 6667, ScudBotFactory('#' + chan,nickname="scudian"))
    reactor.run()
from model.bot import Bot, db, engine, database, ModelException


class BotManager:
    def __init__(self, networkManager, channelManager):
        self.networkManager = networkManager
        self.channelManager = channelManager

    def add(self, nick, network_name):
        if network_name is None or len(network_name.strip()) == 0:
            raise ModelException("Network required when adding a bot.")

        network = self.networkManager.add(network_name)

        if(network is None):
            raise ModelException("Unable to get or add network " + network_name)

        bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network == network).first()
        if bot is not None:
            return bot

        bot = Bot(nick, network_name)
        db.add(bot)
        if not database.commit():
            raise ModelException("Error during commit of Bot "+ nick +" for network " + network_name)
        return bot

    def addChannel(self, bot_name, channel_name):
        #add/get the channel
        channel = self.channelManager.add(channel_name)
        #get the bot
        bot = Bot.query.filter(Bot.nick == bot_name).first()
        if bot is None:
            return None
        #add channel to bot
        bot.channels.append(channel)
        #commit
        database.commit()

    def delete(self, nick, network_name):
        bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network_name == network_name).first()
        if bot is None:
            return
        db.delete(bot)
        print "Committing deletion of %s, %s" % (nick, network_name)
        database.commit()

    def output(self, name=None):
        if name is not None:
            bots = Bot.query.filter(Bot.nick==name).all()
        else:
            bots = Bot.query.all()

        for bot in bots:
            print bot
            for server in bot.network.servers:
                print "on: \t%s" % server
            for channel in bot.channels:
                print "in: \t%s" % channel
        print ""

        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        database.commit()
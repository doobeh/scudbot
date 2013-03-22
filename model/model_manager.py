#from model import Network, Server, Channel, Bot, Admin#, User, Message, Url
# Import the different database modules
from bot import User, Network, Server, Channel, Bot, db, engine, database, ModelException
from sqlalchemy.exc import IntegrityError

engine.echo = False


class ModelManager:
    def init_db(self):
        database.init_db()

    #PRINT METHODS
    #Print out the database
    def printAll(self):
        print "Bots:"
        self.printBot()
        print "Users:"
        self.printUsers()
        print "Finished Printing"

    def printBot(self, name=None):
        if name is not None:
            bots = Bot.query.filter(Bot.nick == name).all()
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
        db.commit()

    def printNetworks(self):
        for network in Network.query.all():
            print network
            for server in network.servers:
                print "\t%s" % server
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        db.commit()

    def printServers(self):
        for server in Server.query.all():
            print server
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        db.commit()

    def printChannels(self):
        for channel in Channel.query.all():
            print channel
            for bot in channel.bots:
                print "\t%s" % bot
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        db.commit()

    def printUsers(self):
        for user in User.query.all():
            print user
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        db.commit()

    #END PRINT METHODS

    def commit(self):
        try:
            db.commit()
            return True
        except IntegrityError as (statement):
            #Write out error
            print "IntegrityError \"{0}\" for {1}".format(statement.orig, statement.params)
            #Rollback
            db.rollback()
            #Raise new Exception
            if statement.connection_invalidated:
                print "Program error, connection invalidated to Database, quitting"
            return False

    #Add Methods
    def addBot(self, nick, network_name):
        if network_name is None or len(network_name.strip()) == 0:
            raise ModelException("Network required when adding a bot.")

        network = self.addNetwork(network_name)

        bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network == network).first()
        if bot is not None:
            return bot

        bot = Bot(nick, network_name)
        db.add(bot)
        if not self.commit():
            raise ModelException("Error during commit of Bot " + nick + " for network " + network_name)
        print "Committing add of %s to %s" % (nick, network_name)
        return bot

    def addServer(self, network_name, address, port=None, SSL=False):
        server = Server.query.filter(Server.address == address).first()
        if server is not None:
            return server

        #Make sure the network exists
        self.addNetwork(network_name)

        if port is None or len(port.strip()) == 0:
            port = None
        else:
            port = int(port)
        server = Server(network_name, address, port, SSL)
        db.add(server)
        if self.commit():
            #TODO work out how to print out the server here using the toString shit
            raise ModelException("Problem committing server " + str(server))
        print "Committing add of %s to %s" % (address, network_name)
        return server

    def addNetwork(self, network_name):
        network = Network.query.filter(Network.name == network_name).first()
        if network is not None:
            return network
        network = Network(network_name)
        db.add(network)
        if not self.commit():
            raise ModelException("Problem committing network " + network_name)
        print "Committing add of %s" % network_name
        return network

    def addChannel(self, name):
        channel = Channel.query.filter(Channel.name == name).first()
        if channel is not None:
            return channel
        channel = Channel(name)
        db.add(channel)
        if not self.commit():
            raise ModelException("Problem committing channel " + name)
        print "Committing add of %s" % name
        return channel

    def addChannelBot(self, channel_name, nick, network_name):
        #add/get the channel
        channel = self.addChannel(channel_name)
        #get the bot
        bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network_name == network_name).first()
        if bot is None:
            return None
            #add channel to bot
        bot.channels.append(channel)
        #commit
        print "Committing deletion of %s from %s on %s" % (channel_name, nick, network_name)
        self.commit()

    def addUser(self, nick):
        user = User.query.filter(User.nick == nick).first()
        if user is not None:
            return user
        user = User(nick)
        db.add(user)
        if not self.commit():
            raise ModelException("Problem committing user with nick " + nick)
        print "Committing deletion of %s" % nick
        return user

    #Delete methods   
    def delBot(self, nick, network_name):
        bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network_name == network_name).first()
        if bot is None:
            return
        db.delete(bot)
        print "Committing deletion of %s, %s" % (nick, network_name)
        self.commit()

    def delNetwork(self, network_name):
        network = Network.query.filter(Network.name == network_name).first()
        if network is None:
            return
            #If we found the network then there might be bots that use it
        bots = Bot.query.filter(Bot.network_name == network_name).all()
        if len(bots) > 0:
            print "Found bots that reference the network:"
            for bot in bots:
                print bot.nick
            func_name = raw_input("Delete network and bots? [Y/n]")
            if func_name != "Y" and func_name != "y":
                print "Aborting deletion of %s" % network_name
                return
            for bot in bots:
                print "Deleting %s" % bot.nick
                db.delete(bot)
        db.delete(network)
        print "Committing deletion of %s" % network_name
        self.commit()

    def delChannel(self, channel_name):
        #add/get the channel
        channel = Channel.query.filter(Channel.name == channel_name).first()
        if channel is None:
            print "Unable to find channel: %s" % channel_name
            return
            #get the bots that reference the channel
        if len(channel.bots) > 0:
            print "Found bots that reference the channel:"
            for bot in channel.bots:
                print bot.nick
        db.delete(channel)
        #commit
        print "Committing deletion of %s" % channel_name
        self.commit()

    def delChannelBot(self, channel_name, nick, network_name):
        #Get the bot
        bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network_name == network_name).first()
        if bot is None:
            print "Unable to find bot: %s on %s" % (nick, network_name)
            return
        channel = Channel.query.filter(Channel.name == channel_name).first()
        if channel is None:
            print "Unable to find channel: %s" % channel_name
            return
        bot.channels.remove(channel)
        #commit
        print "Committing deletion of %s from %s on %s" % (channel_name, nick, network_name)
        self.commit()

    def delUser(self, nick):
        user = User.query.filter(User.nick == nick).first()
        if user is None:
            return
        db.delete(user)
        print "Committing deletion of %s" % user
        self.commit()
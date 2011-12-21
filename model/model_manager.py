#from model import Network, Server, Channel, Bot, Admin#, User, Message, Url
# Import the different database modules
from bot import Network, Server, Channel, Bot, db, engine
from sqlalchemy.exc import IntegrityError

engine.echo = False

class ModelManager:
    
    #PRINT METHODS
    #Print out the database
    def printAll(self):
        self.printBot()
    
    def printBot(self, name=None):
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
    #END PRINT METHODS
                

    def commit(self):
        try:
            db.commit()
        except IntegrityError as (statement):
            db.rollback()
            print "IntegrityError \"{0}\" for {1}".format(statement.orig, statement.params)
            if(statement.connection_invalidated):
                print "Program error, connection invalidated to Database, quitting"
                quit()
            return False
        else:
            return True
    
    '''
    def addAdmin(self, name):
        admin = Admin(name)
        db.add(admin)
        return self.commit()'''
           
    def addOrGetBot(self, nick, network_name=None):
        if network_name is not None:
            network = Network.query.filter(Network.name == network_name).first()
            if network is not None:
                bot = Bot.query.filter(Bot.nick == nick).filter(Bot.network == network).first()
                if bot is not None:
                    return bot
            else:
                network = Network(network_name)
                db.add(network)
                if not self.commit():
                    return None
                
            bot = Bot(nick, network_name)
            db.add(bot)
            if self.commit():
                return bot
        return None
    
    def addOrGetServer(self, network_name, address, port=None, SSL=False):
        server = Server.query.filter(Server.address == address).first()
        if(server is not None):
            return server
        
        #Make sure the network exists
        network = Network.query.filter(Network.name == network_name).first()
        if network is None:
            network = Network(network_name)
            db.add(network)
            if not self.commit():
                return None
            print "Network %s added" % network_name
        if(port is None or len(port.strip()) == 0):
            port = None
        else:
            port = int(port)
        server = Server(network_name, address, port, SSL)
        db.add(server)
        if self.commit():
            return server
        return None
    
    def addOrGetNetwork(self, network_name):
        network = Network.query.filter(Network.name == network_name).first()
        if network is not None:
            return network
        network = Network(network_name)
        db.add(network)
        if self.commit():
            return network
        
    def addOrGetChannel(self, name):
        channel = Channel.query.filter(Channel.name == name).first()
        if channel is not None:
            return channel
        channel = Channel(name)
        db.add(channel)
        if self.commit():
            return channel
        
    def addChannelToBot(self, channel_name, bot_name):
        #get the channel
        channel = Channel.query.filter(Channel.name == channel_name).first()
        if channel is None:
            return
        #get the bot
        bot = Bot.query.filter(Bot.nick == bot_name).first()
        if bot is None:
            return None
        #add channel to bot
        bot.channels.add(channel)
        #commit
        self.commit()
        
    def delNetwork(self, network_name):
        network = Network.query.filter(Network.name == network_name).first()
        if network is None:
            return
        #If we found the network then there might be bots that use it
        bots = Bot.query.filter(Bot.network_name == network_name).all()
        if(len(bots) > 0):
            print "Found bots that reference the network:"
            for bot in bots:
                print bot.nick
            func_name = raw_input("Delete network and bots? [Y/n]")
            if(func_name != "Y" and func_name != "y"):
                print "Aborting deletion of %s" % network_name
                return
            for bot in bots:
                print "Deleting %s" % bot.nick
                db.delete(bot)
        db.delete(network)
        print "Committing deletion of %s" % network_name
        self.commit()
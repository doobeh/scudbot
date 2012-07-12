from model.bot import Bot, Network, db, engine, database, ModelException

class NetworkManager:
    
    def add(self, network_name):
        network = Network.query.filter(Network.name == network_name).first()
        if network is not None:
            return network
        network = Network(network_name)
        db.add(network)
        if not database.commit():
            raise ModelException("Problem committing network " + network_name)
        return network
    
    def delete(self, network_name):
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
        database.commit()
    
    def output(self):
        for network in Network.query.all():
            print network
            for server in network.servers:
                print "\t%s" % server
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        database.commit()
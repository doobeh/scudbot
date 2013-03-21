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

    def delete(self, network_name, deleteBot = False):
        network = Network.query.filter(Network.name == network_name).first()
        if network is None:
            return
        #If we found the network then there might be bots that use it
        bots = Bot.query.filter(Bot.network_name == network_name).all()
        if(len(bots) > 0):
            if(not deleteBot):
                return
            for bot in bots:
                print "Deleting %s" % bot.nick
                db.delete(bot)
        db.delete(network)
        print "Committing deletion of %s" % network_name
        database.commit()

    def __str__(self):
        #http://www.skymind.com/~ocrow/python_string/
        from cStringIO import StringIO
        ret_str = StringIO()

        for network in Network.query.all():
            ret_str.write(str(network))
            for server in network.servers:
                ret_str.write("\n\t")
                ret_str.write(str(server))
        ret_str.write("\n")
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        database.commit()
        return ret_str.getvalue()
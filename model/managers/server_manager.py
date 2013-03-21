from model.bot import Bot, Server, db, database, engine, database, ModelException

class ServerManager:

    def __init__(self, networkManager):
        self.networkManager = networkManager

    def add(self, network_name, address, port=None, SSL=False):
        server = Server.query.filter(Server.address == address).first()
        if(server is not None):
            return server

        #Make sure the network exists
        network = self.networkManager.add(network_name)

        if(port is None or len(port.strip()) == 0):
            port = None
        else:
            port = int(port)
        server = Server(network_name, address, port, SSL)
        db.add(server)
        if not database.commit():
            raise ModelException("Problem committing server " + str(server))
        return server

    def delete(self, address):
        server = Server.query.filter(Server.address == address).first()
        if server is None:
            return server
        db.delete(server)
        print "Committing deletion of %s, %s" % (address)
        database.commit()

    def clean(self):
        servers = Server.query.filter(Server.network == None).all()
        for server in servers:
            db.delete(server)
        database.commit()

    def output(self):
        for server in Server.query.all():
            print server
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        database.commit()
from model.bot import Channel, db, engine, database, ModelException

class ChannelManager():
    
    def add(self, name):
        channel = Channel.query.filter(Channel.name == name).first()
        if channel is not None:
            return channel
        channel = Channel(name)
        db.add(channel)
        if not database.commit():
            raise ModelException("Problem committing channel " + name)
        return channel
    
    def delete(self, name):
        #add/get the channel
        channel = Channel.query.filter(Channel.name == channel_name).first()
        if channel is None:
            print "Unable to find channel: %s" % channel_name
            return
        #get the bots that reference the channel
        if(len(channel.bots) > 0):
            print "Found bots that reference the channel:"
            for bot in channel.bots:
                print bot.nick
        db.delete(channel)
        #commit
        database.commit()
    
    def output(self):
        for channel in Channel.query.all():
            print channel
            for bot in channel.bots:
                print "\t%s" % bot
        print ""
        #This seems like a hack to make sure we don't store any
        #references in memory which get used, modified later on
        database.commit()
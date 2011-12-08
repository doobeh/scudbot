from ModelManager import ModelManager

manager = ModelManager()

def usage(args):
    print("")
    print("Commands:")
    print("help: Prints this message")
    print("list: Prints what's inside the database")
    print("add:  Adds a Bot witwh a Network")
    print("edit: Edits a Bot")
    print("quit: quits the program")
    print("")

def list(args):
    if(args == '?'):
        print "Lists aspects of the database."
        print "list bot [name]: Lists the name of the bot or all the bots"
        print "list networks: lists all the networks."
        print "list servers: lists all the servers."
        print "list channels: lists all the channels."
        print "list: lists the whole database"
        return
    #find the occurence of the first space
    if(args is None or len(args.strip()) == 0):
        manager.printAll()
    else:
        args = args.strip().split(' ')
        if(len(args) > 0):
            if(args[0] == 'bot' or args[0] == 'bots'):
                if(len(args) == 2):
                    manager.printBot(args[1])
                else:
                    manager.printBot()
            elif(args[0] == 'networks'):
                manager.printNetworks()
            elif(args[0] == 'servers'):
                manager.printServers()
            elif(args[0] == 'channels'):
                manager.printChannels()
            else:
                print "Unknown list command: %s" % args[0]
                list('?')
        else:
            print args

def add(args):
    if(args == '?'):
        print "Add a bot, network or channel to the database."
        print "add bot nick network: Adds a bot to watch a given network."
        print "add network name: Adds a network with the given name."
        print "add server network address[:port[=SSL]]: Adds a server."
        print "add channel name: Adds a channel with \"name\" to the channel database."
        print "add chantobot channel bot: Adds a server."
        return
    else:
        if(args is None or len(args.strip()) == 0):
            print "No command given to add, please specify a valid command."
            add('?')
            return
        args = args.strip().split(' ')
        if(len(args) > 0):
            if(args[0] == 'bot'):
                if(len(args) != 3):
                    print "Cannot add bot without the correct number of arguments."
                    print "add bot nick network: Adds a bot to watch a given network."
                    print "add %s" % (args)
                    return
                bot = manager.addOrGetBot(args[1], args[2])
                if(bot is not None):
                    print "Bot %s added" % bot
                    return
                print "Bot %s not added with network %s" % (args[1], args[2])
            elif(args[0] == 'network'):
                if(len(args) != 2):
                    print "Cannot add network without the correct number of arguments."
                    print "add network name: Adds a network with the given name."
                    print "add %s" % (args)
                    return
                network = manager.addOrGetNetwork(args[1])
                if(network is not None):
                    print "Network %s added" % network
                    return
                print "Network %s not added" % args[1]
            elif(args[0] == 'channel'):
                if(len(args) != 2):
                    print "Cannot add channel without the correct number of arguments."
                    print "add channel name: Adds a channel with \"name\" to the channel database."
                    print "add %s" % (args)
                    return
                channel = manager.addOrGetChannel(args[1])
                if(channel is not None):
                    print "Channel %s added" % channel
                    return
                print "Channel %s not added" % args[1]
            elif(args[0] == 'server'):
                if(len(args) != 3):
                    print "Cannot add server without the correct number of arguments."
                    print "add server network address[:port[=SSL]]: Adds a server."
                    print "add %s" % (args)
                    return
                #Split out the second argument to address, port, SSL
                #User regexp to do this eventually
                network_name = args[1]
                args = args[2].strip().split(':')
                if(len(args) > 1):
                    address = args[0]
                    args = args[1].strip().split('=')
                    if(len(args) == 2):
                        port = args[0]
                        SSL = True
                    else:
                        port = args[1]
                        SSL = False
                else:
                    address = args[0]
                    port = None
                    SSL = False
                #Get rid of the above ugly code and replace with Regexp
                
                server = manager.addOrGetServer(network_name, address, port, SSL)
                if(server is not None):
                    print "Server %s added" % server
                    return
                print "Server %s not added" % args[1]
            elif(args[0] == 'chantobot'):
                if(len(args) != 3):
                    print "Cannot add channel to bot without the correct number of arguments."
                    print "add chantobot channel bot: Adds a server."
                    print "add %s" % (args)
                    return
                manager.addChannelToBot(args[1], args[2])
            else:
                print "Unknown add command: %s" % args[0]
                add('?')
        else:
            print args
            

#List of all the functions that can be used
function_map = {'help' : usage,
                'list' : list,
                'add'  : add,
                'quit' : quit}

while True:
    func_name = raw_input("Command:")
    args = None
    first_space = func_name.find(' ')
    if(first_space > 0):
        args = func_name[first_space+1:]
        func_name = func_name[0:first_space]
    function = function_map.get(func_name, None)
    if function is None:
        print "Unknown command %s" % func_name
        usage(args)
    else:
        function(args)
'''
name = raw_input("Enter bot name:")
server = raw_input("Enter server address:")
port = int(raw_input("Enter server port:"))

print "Starting creation of %s, on %s:%d" % (name, server, port)
bot = manager.addOrGetBot(name, server, port)
if(bot is None):
    print "Bot was not created"
    quit()
channel = raw_input("Add a channel:")
manager.addChannel(bot, channel)
manager.commit()

manager.printDB()
'''
quit()

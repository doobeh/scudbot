from model import ModelManager
manager = ModelManager()


#TODO Add URLs
#TODO Add Edit
def usage(args):
    print("")
    print("Commands:")
    print("help: Prints this message")
    print("list: Prints what's inside the database")
    print("add:  Adds a Bot with a Network")
    print("del:  Deletes a Bot, Network, Channel, Server")
    print("edit: Edits a Bot")
    print("quit: quits the program")
    print("")


def list_database(args):
    if args == '?':
        print "Lists aspects of the database."
        print "list bot [name]: Lists the name of the bot or all the bots"
        print "list networks: lists all the networks."
        print "list servers: lists all the servers."
        print "list channels: lists all the channels."
        print "list users: lists all the users."
        print "list: lists the whole database"
        return
    #find the occurence of the first space
    if args is None or len(args.strip()) == 0:
        manager.printAll()
    else:
        args = args.strip().split(' ')
        if len(args) > 0:
            if args[0] == 'bot' or args[0] == 'bots':
                if len(args) == 2:
                    manager.printBot(args[1])
                else:
                    manager.printBot()
            elif args[0] == 'networks':
                manager.printNetworks()
            elif args[0] == 'servers':
                manager.printServers()
            elif args[0] == 'channels':
                manager.printChannels()
            elif args[0] == 'users':
                manager.printUsers()
            else:
                print "Unknown list command: %s" % args[0]
                list_database('?')
        else:
            print args


# TODO Check Del bot
# TODO Add Del server
# TODO Add Del chantobot
def delete(args):
    if args == '?':
        print "Delete a bot, network, server or channel from the database."
        print "del bot nick network: Deletes a bot."
        print "del network name: Deletes a network."
        print "del server network address[:port[=SSL]]: Deletes a server."
        print "del channel name: Deletes a channel with \"name\" from the channel database."
        print "del chanbot channel bot network: Deletes a channel from a bot."
        print "del user name: Deletes a user from the database."
        return
    else:
        if args is None or len(args.strip()) == 0:
            print "No command given to del, please specify a valid command."
            delete('?')
            return
        args = args.strip().split(' ')
        if len(args) > 0:
            if args[0] == 'bot':
                if len(args) != 3:
                    print "Cannot delete bot without the correct number of arguments."
                    print "del bot nick network: Deletes a bot."
                    print "del %s" % args
                    return
                manager.delBot(args[1], args[2])
            elif args[0] == 'network':
                if len(args) != 2:
                    print "Cannot delete network without the correct number of arguments."
                    print "del network name: Deletes a network."
                    print "del %s" % args
                    return
                manager.delNetwork(args[1])
            elif args[0] == 'channel':
                if len(args) != 2:
                    print "Cannot delete channel without the correct number of arguments."
                    print "del channel name: Deletes a channel with \"name\" from the channel database."
                    print "del %s" % args
                    return
                manager.delChannel(args[1])
            elif args[0] == 'chanbot':
                if len(args) != 4:
                    print "Cannot delete a channel from a bot without the correct number of arguments."
                    print "del chanbot channel bot network: Deletes a channel from a bot."
                    print "del %s" % args
                    return
                manager.delChannelBot(args[1], args[2], args[3])
            elif args[0] == 'user':
                if len(args) != 2:
                    print "Cannot delete a user without the correct number of arguments."
                    print "del user name: Adds a user with \"name\" from the user database."
                    print "del %s" % args
                    return
                manager.delUser(args[1])
            else:
                print "Invalid command, please specify a valid command."
                delete('?')
        return


def add(args):
    if args == '?':
        print "Add a bot, network or channel to the database."
        print "add bot nick network: Adds a bot to watch a given network."
        print "add network name: Adds a network with the given name."
        print "add server network address[:port[=SSL]]: Adds a server."
        print "add channel name: Adds a channel with \"name\" to the channel database."
        print "add chanbot channel bot network: Adds a channel to a bot."
        print "add user nick: Adds a user to the database."
        print "add msg nick network message: Adds a message to the database for a user."
        return
    else:
        if args is None or len(args.strip()) == 0:
            print "No command given to add, please specify a valid command."
            add('?')
            return
        args = args.strip().split(' ')
        if len(args) > 0:
            if args[0] == 'bot':
                if len(args) != 3:
                    print "Cannot add bot without the correct number of arguments."
                    print "add bot nick network: Adds a bot to watch a given network."
                    print "add %s" % args
                    return
                bot = manager.addBot(args[1], args[2])
                if bot is not None:
                    print "Bot %s added" % bot
                    return
                print "Bot %s not added with network %s" % (args[1], args[2])
            elif args[0] == 'network':
                if len(args) != 2:
                    print "Cannot add network without the correct number of arguments."
                    print "add network name: Adds a network with the given name."
                    print "add %s" % args
                    return
                network = manager.addNetwork(args[1])
                if network is not None:
                    print "Network %s added" % network
                    return
                print "Network %s not added" % args[1]
            elif args[0] == 'channel':
                if len(args) != 2:
                    print "Cannot add channel without the correct number of arguments."
                    print "add channel name: Adds a channel with \"name\" to the channel database."
                    print "add %s" % args
                    return
                channel = manager.addChannel(args[1])
                if channel is not None:
                    print "Channel %s added" % channel
                    return
                print "Channel %s not added" % args[1]
            elif args[0] == 'server':
                if len(args) != 3:
                    print "Cannot add server without the correct number of arguments."
                    print "add server network address[:port[=SSL]]: Adds a server."
                    print "add %s" % args
                    return
                #Split out the second argument to address, port, SSL
                #User regexp to do this eventually
                network_name = args[1]
                args = args[2].strip().split(':')
                if len(args) > 1:
                    address = args[0]
                    args = args[1].strip().split('=')
                    if len(args) == 2:
                        port = args[0]
                        SSL = True
                    else:
                        port = args[0]
                        SSL = False
                else:
                    address = args[0]
                    port = None
                    SSL = False
                #Get rid of the above ugly code and replace with Regexp

                server = manager.addServer(network_name, address, port, SSL)
                if server is not None:
                    print "Server %s added" % server
                    return
                print "Server %s not added" % args[1]
            elif args[0] == 'chanbot':
                if len(args) != 4:
                    print "Cannot add channel to bot without the correct number of arguments."
                    print "add chanbot channel bot network: Adds a channel to a bot."
                    print "add %s" % args
                    return
                manager.addChannelBot(args[1], args[2], args[3])
            elif args[0] == 'user':
                if len(args) != 2:
                    print "Cannot add user without the correct number of arguments."
                    print "add user nick: Adds a user to the database."
                    print "add %s" % args
                    return
                user = manager.addUser(args[1])
                if user is not None:
                    print "User %s added" % user
                    return
                print "User %s not added" % args[1]
            elif args[0] == 'msg':
                if len(args) < 4:
                    print "Cannot add message without the correct number of arguments."
                    print "add msg nick network message: Adds a message to the database for a user."
                    print "add %s" % args
                    return
                user = manager.addMessage(args[1], args[2], args[3], " ".join(args[4:]))
                if user is not None:
                    print "User %s added" % user
                    return
                print "User %s not added" % args[1]
            else:
                print "Unknown add command: %s" % args[0]
                add('?')
        else:
            print args


#List of all the functions that can be used
function_map = {'help': usage,
                'list': list_database,
                'add': add,
                'del': delete,
                'quit': quit}

while True:
    manager.init_db()
    func_name = raw_input("Command:")
    args = None
    first_space = func_name.find(' ')
    if first_space > 0:
        args = func_name[first_space + 1:]
        func_name = func_name[0:first_space]
    function = function_map.get(func_name, None)
    if function is None:
        print "Unknown command %s" % func_name
        usage('')
    else:
        function(args)
quit()
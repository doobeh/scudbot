from model.managers import BotManager, NetworkManager, ServerManager, ChannelManager, init_db

networkManager = NetworkManager
botManager = BotManager
serverManager = ServerManager
channelManager = ChannelManager

init_db()

botManager.add("scud", "0xff")
botManager.output("scud")

botManager.delete("scud", "0xff")
botManager.add("scud", "0xff")
botManager.output("scud")

channelManager.add("#scud.test")

botManager.addChannel("scud", "#scud.test")

serverManager.add("0xff", "irc.0xff.com", "6697", True)
botManager.output("scud")
serverManager.output()

networkManager.delete("0xff")
print "bots"
botManager.output()
print "networks"
networkManager.output()
print "servers"
serverManager.output()
print "channels"
channelManager.output()
print "Cleaning Servers"
serverManager.clean()
print "Servers"
serverManager.output()

quit()

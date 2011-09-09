from model import Network, Channel, Bot, NetworkChannel, User, Message, Url
# Import the different database modules
from scud import app
from database import db_session as db
from model import *

# Create some networks:
qnet = Network('uk.quakenet.org',6667)
fnode = Network('irc.freenode.com',6667)

# Some Channels
fuk = Channel('fortress.uk')
ea = Channel('fortress.uk.ea')

# A Bot
scud = Bot('scud')

# Create an active 'botchannel'
qnet_fuk = NetworkChannel(fuk,qnet) # Scud monitors fortress.uk on QuakeNet.
qnet_ea = NetworkChannel(ea,qnet) # Scud monitors fortress.uk.ea on Quakenet.
fnode_fuk = NetworkChannel(fuk,fnode) # Scud monitors fortress.uk on FreeNode.

#Add Qnet FUK as a network channel for Scud
scud.network_channels.add(qnet_fuk)

db.add_all([qnet,fnode,fuk,ea,scud,qnet_fuk,qnet_ea,fnode_fuk])  # add them all to database.
db.commit()

#Add the qnet_ea as a NetworkChannel for Scud
scud.network_channels.add(qnet_ea)
db.commit()

#Create a second bot
scud2 = Bot('scud2')
#Reassign the QuakeNet Fortress.UK channel to the second  bot
scud2.network_channels.add(qnet_fuk)
#Add and commit the second bot
db.add(scud2)
db.commit()

#At this point we have
#Scud - QNet - #fortress.uk.ea
#Scud2 - QNet - #fortress.uk
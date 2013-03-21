from model.bot import database

import network_manager
NetworkManager = network_manager.NetworkManager()

import server_manager
ServerManager = server_manager.ServerManager(NetworkManager)

import channel_manager
ChannelManager = channel_manager.ChannelManager()

import bot_manager
BotManager = bot_manager.BotManager(NetworkManager, ChannelManager)

def init_db():
    database.init_db()
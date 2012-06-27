import database
db = database.db_session
engine = database.engine

import channel
Channel = channel.Channel

import server
Server = server.Server

import network
Network = network.Network

import bot
Bot = bot.Bot

import user
User = user.User

import message
Message = message.Message

'''
import url
Url = url.Url

import message
Message = message.Message
'''

def check_existing(context):
    ''' Checks database to see if url link has been mentioned before.

        When a Url object is created, this function checks the existing
        database to see if the link has been mentioned before, if it
        has, it returns the 'original' Url id, which is stored against
        the new Url.
        
    '''

    item = Url.query.filter_by(url=context.current_parameters['url']).filter(Url.original_id == None).first()
    if item:
        return item.id
    return None






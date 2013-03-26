# Scudbot introduction

## Requires:
* Flask
* Twisted
* Flask-SQLAlchemy

## TODO
* Add webpage back
* Fix all references so they use IDs and backreferences correctly
* Fix the bot to use the new database model

## Basic Operation:
Scudbot is divided into two programs, ircbot.py, which launches IRC clients to monitor public messages in channels of
your choice, and scud.py which is the webapp showing a nice view on the data captured and processed by the application.

If you're starting from scratch, you'll need to initialize the database by running dbsetup.py, this will create
enough example information within the database to get it all running.

Then run ircbot.py to launch the IRC bot(s), and scud.py to run the web application.  You should be able to access
the webapp at http://127.0.0.1:5000

## Other Notes

Want to use the following for messages in a channel
http://www.humblesoftware.com/finance/documentation


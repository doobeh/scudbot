# Scudbot introduction

## Requires:
* Flask
* Twisted
* Flask-SQLAlchemy

## TODO
* Fix the formatting on urls so it looks nicer
* Separate ident into Nick, Ident and Host
* A more contrasting colour scheme
* Fix all links so they point to locations
* Add network to Url Model.

## Basic Operation:
Scudbot is divided into two programs, ircbot.py, which launches IRC clients to monitor public messages in channels of
your choice, and scud.py which is the webapp showing a nice view on the data captured and processed by the application.

If you're starting from scratch, you'll need to initialize the database by running dbsetup.py, this will create some
enough example information within the database to get it all running.

Then run ircbot.py to launch the IRC bot(s), and scud.py to run the web application.  You should be able to access
the webapp at http://127.0.0.1:5000

## Other Notes


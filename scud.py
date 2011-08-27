from twisted.words.protocols import irc
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

from flask import Flask, render_template
from model import Message

app = Flask(__name__)

SECRET_KEY = 'asdkjad98a7sd8asd98h983h9732e2387ey682jhbd23jhb328o726387623987d62873dg23dgu2gdjh2g38327dto283d7t'
DEBUG = True

app.config.from_object(__name__) # load uppercase keys as config options.

from database import db_session, init_db
init_db()

@app.route("/")
def index():
    m = Message.query.all()
    return render_template('index.html',messages=m)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

resource = WSGIResource(reactor, reactor.getThreadPool(), app) # register app with reactor.
site = Site(resource)
reactor.listenTCP(80, site)  # site will listen on local server at port 80

class MomBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)

    def joined(self, channel):
        print "Joined %s." % (channel,)

    def privmsg(self, user, channel, msg):
        if not user:
            return
        m = Message(user, channel, msg)
        db_session.add(m)
        db_session.commit()
        

class MomBotFactory(protocol.ClientFactory):
    protocol = MomBot

    def __init__(self, channel, nickname='YourMomDotCom'):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
        


if __name__ == "__main__":
    chan = "fortress.uk.scud"
#    reactor.connectTCP('uk.quakenet.org', 6667, MomBotFactory('#' + chan,nickname="scudia"))
    reactor.run()
#    app.run()
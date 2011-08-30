from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site

from flask import Flask, render_template

from bot.ScudBot import ScudBotFactory
from database import db_session, init_db
from model import Message, Admin, Url

init_db()

app = Flask(__name__)

SECRET_KEY = 'asdkjad98a7sd8asd98h983h9732e2387ey682jhbd23jhb328o726387623987d62873dg23dgu2gdjh2g38327dto283d7t'
DEBUG = True

app.config.from_object(__name__) # load uppercase keys as config options.

@app.route("/")
def index():
    m = Message.query.all()
    return render_template('index.html',messages=m)

@app.route("/urls/")
def urls():
    u = Url.query.all()
    return render_template('urls.html',urls=u)

@app.route("/dataload/")
def dataload():
    u = Admin("doobeh!~quassel@b33f.net")
    db_session.add(u)
    db_session.commit()
    
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

resource = WSGIResource(reactor, reactor.getThreadPool(), app) # register app with reactor.
site = Site(resource)
reactor.listenTCP(8080, site)  # site will listen on local server at port 80

if __name__ == "__main__":
    chan = "fortress.uk.scud"
    reactor.connectTCP('uk.quakenet.org', 6667, ScudBotFactory('#' + chan,nickname="scudia"))
    reactor.run()
#    app.run()
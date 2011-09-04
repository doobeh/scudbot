from flask import Flask, render_template, redirect, flash, url_for
from database import db_session, init_db
from model import Message, Admin, Url
from random import choice
from jinja2.utils import generate_lorem_ipsum

init_db()

app = Flask(__name__)

SECRET_KEY = 'asdkjad98a7sd8asd98h983h9732e2387ey682jhbd23jhb328o726387623987d62873dg23dgu2gdjh2g38327dto283d7t'
DEBUG = True

app.config.from_object(__name__) # load uppercase keys as config options.

@app.route("/")
def index():
    m = Message.query.all()
    return render_template('index.html',messages=m)

@app.route("/images/")
def images():
    i = Url.query.filter_by(img_cached=True).all()
    return render_template('images.html',images=i)

@app.route("/urls/")
def urls():
    u = Url.query.all()
    return render_template('urls.html',urls=u)

@app.route("/dataload/")
def dataload():
    
    # Create fake messages:
    names = ('alice','bob','clive','dave','enid','frank','george')
    hosts = ('b33f.net','google.com','brah.com')
    channels = ('fortress.uk.scud','fortress.uk.ea')
    
    for i in range(1000):
        name = choice(names)         
        user = '%s!~%s@%s' % (name,name,choice(hosts),) # Format a irc 'user/host'
        m = Message(user, choice(channels), generate_lorem_ipsum(1,html=False,min=5,max=25))
        db_session.add(m)
    db_session.commit()
        
    # Create admins:
    admins = ('WeiGonChi!~seph@miaows.eu','doobeh!~quassel@b33f.net')
    [db_session.add(Admin(u)) for u in admins]
    db_session.commit()
    
    flash("Data loaded")
    return redirect(url_for('index'))
    

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.run()
from flask import Flask, render_template, redirect, flash, url_for, request, abort
from flaskext.login import LoginManager, login_user, login_required, fresh_login_required, logout_user
from forms.LoginForm import LoginForm
from database import db_session, init_db
from model import *
from random import choice
from jinja2.utils import generate_lorem_ipsum
from math import ceil
import settings
import urllib

init_db()

app = Flask(__name__)

#Create the login manager
login_manager = LoginManager()
#Setup the app in the login_manager
login_manager.setup_app(app)

SECRET_KEY = 'asdkjad98a7sd8asd98h983h9732e2387ey682jhbd23jhb328o726387623987d62873dg23dgu2gdjh2g38327dto283d7t'
DEBUG = True

app.config.from_object(__name__) # load uppercase keys as config options.


login_manager.login_view = "login"

##Login Section
@login_manager.user_loader
def load_user(user):
    return Admin.query.get(user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(form.admin)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)

@app.route("/admin")
@login_required
def admin():
    #Bot
    bots = Bot.query.all()
    #Network
    #nworks = Network.query.all()
    #Network Channel
    #Channel
    #User
    return render_template('admin.html', bots=bots)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


##App section
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/images/")
def images():
    i = Url.query.filter(Url.img_cached != None).all()
    return render_template('images.html',images=i)

@app.route("/url/<int:urlId>")
def url(urlId):
    row = Url.query.filter_by(id=urlId).first()
    if row == None:
        flash('No result found...')
        return redirect(url_for('urls'))
    return render_template('urls.html',url=row)

@app.route("/urls/", defaults={'page':1})
@app.route("/urls/page/<int:page>")
def urls(page):
    rows = Url.query.order_by(Url.date_created.desc())
    totalRows = rows.count()
    c = rows.limit(settings.PER_PAGE).offset((page-1)*settings.PER_PAGE)
    if not c.count() and page != 1:
        flash('No results found on requested page... forwarding you here.')
        return redirect(url_for('index',channel=channel))
    pagination = Pagination(page, settings.PER_PAGE, totalRows)
    return render_template('urls.html',urls=c,pagination=pagination)


@app.route("/channels/")
def channels():
    n = Network.query.all()
    return render_template('channels.html',networks=n)

@app.route("/perma/<int:id>/")
def permanent(id):
    m = Message.query.filter_by(id=id).first()
    if m is None:
        flash('Couldn\'t find the message, sorry!')
        return redirect(url_for('index'))
    return render_template('permanent.html',message=m)



@app.route("/channel/<int:channel>/", defaults={'page':1})
@app.route("/channel/<int:channel>/page/<int:page>")
def channel_log(channel,page):
    rows = Url.query.filter(network_channel_id=channel).order_by(Url.date_created.desc())
    rows = Message.query.filter_by(network_channel_id=channel).order_by(Message.id.desc())
    totalRows = rows.count()
    c = rows.limit(settings.PER_PAGE).offset((page-1)*settings.PER_PAGE)
    if not c.count() and page != 1:
        flash('No results found on requested page... forwarding you here.')
        return redirect(url_for('urls',channel=channel))
    pagination = Pagination(page, settings.PER_PAGE, totalRows)
    return render_template('urls.html',urls=c,pagination=pagination)

# Pagination Related
def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

app.jinja_env.globals['url_for_other_page'] = url_for_other_page

@app.template_filter('safeurl')
def safeurl(uri):
   return urllib.quote_plus(uri)
app.jinja_env.globals['safeurl'] = safeurl

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
    

#@app.teardown_request
#def shutdown_session(exception=None):
#    db_session.remove()

if __name__ == "__main__":
    app.run()

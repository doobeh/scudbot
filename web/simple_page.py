"""
    simple_page
    ~~~~~~~~~~~

    A simple blueprint that essentially handles static pages, it'll
    dynamically search for a matching template if called-- if that
    template doesn't exist, it'll feed back a 404.

    Useful for pages like About or Contact, where they're generally
    not fed with user-driven data.

"""

import flask
from jinja2 import TemplateNotFound

simple_page = flask.Blueprint('simple_page', __name__,
                              template_folder='templates')


@simple_page.route('/', defaults={'page': 'home'})
@simple_page.route('/<page>/')
def show(page):
    try:
        return flask.render_template('pages/%s.html' % page)
    except TemplateNotFound:
        flask.abort(404)
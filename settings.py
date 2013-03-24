import os

# Helper to keep paths relative.
_basedir = os.path.abspath(os.path.dirname(__name__))

# Flask General Settings
SECRET_KEY = 'SOMETHING_UNGUESSABLE'
DEBUG = True

# Filesystem Related
IMAGE_DIR = os.path.join(_basedir, '/static/img/')
THUMB_DIR = os.path.join(_basedir, '/static/img/thumb/')

# Pagination
PER_PAGE = 10
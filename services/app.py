
from api.upstream_api import *
from api.server_api import *
from api.cluster_api import *
from bottle import run



run(host='127.0.0.1', port=9000, server='gunicorn',
    reload=True, workers=4, debug=True)
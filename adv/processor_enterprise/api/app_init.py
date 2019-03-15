"Initialization of the flask application, sqlalchemy"
from datetime import timedelta
import os
from flask import Flask, jsonify, session
from flask_pymongo import PyMongo
from processor.helper.json.json_utils import json_from_file
from processor.logging.log_handler import getlogger
from processor_enterprise.api.utils import CONFIGFILE, gettokentimeout
from apscheduler.schedulers.background import BackgroundScheduler

# def setup_logging():
#     "Setup the application wide logging functionality"
#     logformat = '%(asctime)s(%(module)s:%(lineno)4d) - %(message)s'
#     level = os.getenv('LOGLEVEL', 'DEBUG')
#     loglevel = level if level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'] else 'WARNING'
#     logging.basicConfig(level=loglevel, datefmt='%d/%b %H:%M', format=logformat)
#     logger = logging.getLogger(__name__)
#     return logger


# The below will be imported application wide
app = None
db = None
LOGGER = getlogger()
appdata = None
scheduler = None


def get_appdata():
    global appdata
    if not appdata:
        appdata = json_from_file(CONFIGFILE)
        if not appdata:
            appdata = {}
    return appdata


def create_scheduler(apscheduler):
    """Create background scheduler for tests to be scheduled."""
    if not apscheduler:
        return None
    # The "apscheduler." prefix is hard coded
    testscheduler = BackgroundScheduler({
        'apscheduler.jobstores.mongo': {
            'type': 'mongodb'
        },
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.executors.processpool': {
            'type': 'processpool',
            'max_workers': '5'
        },
        'apscheduler.job_defaults.coalesce': 'false',
        'apscheduler.job_defaults.max_instances': '3'
    })
    return testscheduler

def create_db(app):
    "Create the pymongo db and init with app later."
    app.config["MONGO_URI"] = "mongodb://localhost:27017/validator"
    LOGGER.debug("DB URI: %s", app.config['MONGO_URI'])
    appdb = PyMongo(app)
    return appdb


def make_session_permanent():
    "Session timeout set to 600 minutes, we can do it based on configuration too."
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=gettokentimeout())


def index():
    "Main index url for the backend app, an empty json object"
    LOGGER.info("Home:%s", app.config['APPNAME'])
    data = {'status': 'OK', 'app': app.config['APPVERSION']}
    return jsonify(data)


def not_found(error):
    "Any URI not found shall call this API"
    return jsonify({"error": "Unknown, %s" % error, 'status': 'NOK'})


def create_app():
    "Create the flask app and its other configuration, register routes from controllers."
    config = {
        "develop": "config.Development",
        "test": "config.Testing",
        "production": "config.Production",
        "default": "config.BaseConfig"
    }
    myapp = Flask(__name__)
    config_name = os.getenv('CONFIG', 'default')
    LOGGER.info("Config: %s", config_name)
    myapp.config.from_object(config[config_name])
    myapp.before_request(make_session_permanent)
    myapp.register_error_handler(404, not_found)
    myapp.add_url_rule('/', 'index', index)
    return myapp


def unauthorized():
    "Message when authorization fails."
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'Please authenticate to access this API.'})
    response.status_code = 401
    response.headers.set('WWW-Authenticate', "xBasic realm='Authentication Required'")
    return response


def register_modules(myapp):
    "Register all the routes from this function"
    # Register blueprint(s)
    from processor_enterprise.api.apicontroller import MODAPI
    myapp.register_blueprint(MODAPI)


# @pytest.fixture
def initapp(apscheduler=True):
    "The starting point of the flask application, both for debug and production."
    global app, db, scheduler
    LOGGER.info("START")
    scheduler = create_scheduler(apscheduler)
    app = create_app()
    db = create_db(app)
    register_modules(app)
    LOGGER.info("DB, App created!")
    if scheduler:
        scheduler.start()
    return db, app

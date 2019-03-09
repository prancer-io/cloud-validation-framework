"Flask Application config for different setups, mostly data read from the environment variables."
import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    "The base config for all others like Testing, Development and Production"
    DEBUG = False
    TESTING = False
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = os.environ['SESSION_PW'] if 'SESSION_PW' in os.environ else 'whitekitetestenv'
    # Secret key for signing cookies
    SECRET_KEY = os.environ['SESSION_PW'] if 'SESSION_PW' in os.environ else 'whitekitetestenv'
    APPNAME = 'WhiteKite 1.0.0.0, 10-Jan-2019'
    APPVERSION = APPNAME
    APIPREFIX = '/whitekite/api'

    def get_session_key(self):
        "Utility method for SESSION"
        return self.CSRF_SESSION_KEY

    def get_appversion(self):
        "Utility method for APPVERSION"
        return self.APPVERSION


class Development(BaseConfig):
    "Development Configuration, only debug enabled"
    DEBUG = True


class Testing(BaseConfig):
    "Testing enabled for Testing config"
    DEBUG = True
    TESTING = True


class Production(BaseConfig):
    "Disable debug on production"
    DEBUG = False

"Run the local application"
import argparse
import os
from processor.api.app_init import initapp


def run_main():
    "Run it as a server to accept requests"
    _, app = initapp()
    appport = int(os.environ['APPPORT']) if 'APPPORT' in os.environ else 8000
    appdebug = True if 'DEBUG' in os.environ else False
    app.run(host='0.0.0.0', port=appport, debug=appdebug)


if __name__ == "__main__":
    CMDPARSER = argparse.ArgumentParser()
    ARGS = CMDPARSER.parse_args()
    run_main()

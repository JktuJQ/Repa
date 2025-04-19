# Imports
from globals import *

from flask import Flask

from data.db_sesions import sessions

application = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER
)
application.secret_key = FLASK_SECRET_KEY

application.extensions = {
    "db_session": sessions["db"]
}


def run(port: int = 8080, host: str = "127.0.0.1"):
    """Runs application on "http://{host}:{port}/"""
    application.run(port=port, host=host)

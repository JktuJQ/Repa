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
application.debug = DEBUG

application.extensions = {
    "db_session": sessions["db"]
}


def db_session():
    """Возвращает сессию соединения с базой данных"""
    return application.extensions["db_session"]


def run(port: int = 8080, host: str = "127.0.0.1"):
    """Развертывает приложение на "http://{host}:{port}/"""
    application.run(port=port, host=host)

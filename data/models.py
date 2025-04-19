# Imports
from data.db_sesions import databases


# db.sqlite


def load_models():
    """Loads all models from databases"""

    db_database = databases["db"].classes

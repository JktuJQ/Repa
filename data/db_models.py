# Imports
from data.db_sesions import databases


# db.sqlite
User = None

File = None
FileType = None


def load_models():
    """Loads all models from databases"""

    global User, File, FileType

    db_database = databases["db"].classes

    User = db_database.users

    File = db_database.files
    FileType = db_database.file_types

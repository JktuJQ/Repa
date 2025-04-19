# Imports
from data.db_sesions import databases


# db.sqlite
User = None

Note = None
NoteType = None


def load_models():
    """Loads all models from databases"""

    global User, Note, NoteType

    db_database = databases["db"].classes

    User = db_database.users

    Note = db_database.notes
    NoteType = db_database.notes_type

# Import
import typing as t

import sqlalchemy as sa
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import AutomapBase, automap_base

__engines: t.Dict[str, Engine] = dict()
databases: t.Dict[str, AutomapBase] = dict()
sessions: t.Dict[str, Session] = dict()

# First database SHOULD be main database, because `main_session` would be associated with it.
dbs = [r"data\databases\db.sqlite"]


def extract_name(db_file: str) -> str:
    """Extracts name of database from filename."""
    return db_file.split("\\")[-1].split(".")[0]


def full_init(db_files: t.List[str]):
    """
    Invokes `engine_init`, `database_init`, `sessions_init` with pre-defined value `db_names`.
    This function also sets `main_session` variable to match session that is related to first file that was passed.
    """

    global main_session

    engines_init(db_files)

    names = list(__engines.keys())

    databases_init(names)
    sessions_init(names)
    main_session = sessions[extract_name(db_files[0])]


def engines_init(db_files: t.List[str]) -> None:
    """Initializes all engines. Other functions (except for `global_init`) won't work without it."""

    global __engines

    if not db_files:
        raise NameError("No db files found")

    for db_file in db_files:
        database_name = f"sqlite:///{db_file}?check_same_thread=False"

        name = extract_name(db_file)

        __engines[name] = sa.create_engine(database_name)


def databases_init(db_names: t.List[str]):
    """Initializes all databases."""

    global databases

    for name in db_names:
        metadata = sa.MetaData()
        metadata.reflect(__engines[name])

        databases[name] = automap_base(metadata=metadata)
        databases[name].prepare()
        databases[name].metadata.create_all(__engines[name])


def sessions_init(db_names: t.List[str]):
    """Initializes all sessions."""

    global sessions

    for name in db_names:
        sessions[name] = Session(__engines[name])

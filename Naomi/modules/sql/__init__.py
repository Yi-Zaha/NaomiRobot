from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from Naomi import LOGGER as log
DB_URI = "postgres://bovnygnt:HbpZhz6T6Koeub6B-QfpgcIyYD4HpeZU@jelani.db.elephantsql.com/bovnygnt"
if DB_URI and DB_URI.startswith("postgres://"):
    DB_URI = DB_URI.replace("postgres://", "postgresql://", 1)


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8", max_overflow=1000, pool_size=5)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION = start()
except Exception as e:
    exit()

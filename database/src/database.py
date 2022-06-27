import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

host = "localhost" if os.environ.get("DB_HOST") is None else os.environ.get("DB_HOST")
user = "hse" if os.environ.get("POSTGRES_USER") is None else os.environ.get("POSTGRES_USER")
password = "password" if os.environ.get("POSTGRES_PASSWORD") is None else os.environ.get("POSTGRES_PASSWORD")
db = "db" if os.environ.get("POSTGRES_DB") is None else os.environ.get("POSTGRES_DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Model = declarative_base()


class Database:

    @staticmethod
    def get_db():
        database: Session = session()
        try:
            yield database
        finally:
            database.close()

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

host = "localhost" if os.environ.get("DB_HOST") is None else os.environ.get("DB_HOST")
SQLALCHEMY_DATABASE_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" + host + ":5432/{POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Model = declarative_base()


class Database:

    @staticmethod
    def get_db():
        db: Session = session()
        try:
            yield db
        finally:
            db.close()

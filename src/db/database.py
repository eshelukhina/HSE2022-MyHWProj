from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

SQLALCHEMY_DATABASE_URL = "postgresql://hse:password@db:5432/db"

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

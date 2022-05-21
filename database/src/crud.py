from fastapi import Depends
from sqlalchemy.orm import Session

from database.src import tables
from database.src.database import Database


def get_submition(id: int, db: Session = Depends(Database.get_db)):
    return db.query(tables.Submition).filter(tables.Submition.id == id)



from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from library_app.db.database import SessionLocal




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




db_dependency = Annotated[ Session,  Depends(get_db)]
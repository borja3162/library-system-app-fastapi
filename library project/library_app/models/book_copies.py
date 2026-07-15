from enum import StrEnum
from sqlalchemy import Column,Integer , ForeignKey, Enum
from sqlalchemy.orm import relationship

from library_app.db.database import Base






class BookCopyState(StrEnum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
    DAMAGED = "Damaged"
    UNKNOWN =  "Unknown"



class BookCopy(Base):
    __tablename__ = "book_copies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    copy_state = Column(
        Enum(BookCopyState),
        default=BookCopyState.UNKNOWN,
        nullable=False,
    )

    # one to many relationship enforced by foreign key. Could have chosen a foreign key explictly
    # as argument if it was ambiguous
    original_book = relationship(
        "Book",
        back_populates="copies",
        uselist=False
    )




from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship

from library_app.db.database import Base
from library_app.models.book_authors import book_authors

#Book.writers and Author.written_books:  each back_populates points to the attribute on
# the other model. and each represents the same relationship." Python objects will stay synchronized:
# you change one and SQLAlchemy updates the other

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    publication_year = Column(Integer)
    title = Column(String(255))
    isbn = Column(String(17))

    writers = relationship(
        "Author",
        secondary=book_authors,
        back_populates="written_books"
    )

    copies = relationship(
        "BookCopy",
        back_populates="original_book"
    )






from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship


from library_app.models.book_authors import book_authors
from library_app.db.database import Base







class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    year_of_birth = Column(Integer,nullable=True)

    written_books = relationship(
        "Book",
        secondary=book_authors,
        back_populates="writers"
    )


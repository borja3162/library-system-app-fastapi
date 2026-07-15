from sqlalchemy import Column, ForeignKey, Table

from library_app.db.database import Base



#  Object representing a SQL table with less  "Python" and sqlAlchemy tools than classes extending Base.
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),

    Column("book_id", ForeignKey("books.id"), primary_key=True, index=True),

)




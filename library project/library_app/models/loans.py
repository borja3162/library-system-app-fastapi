from sqlalchemy import Column,Integer, ForeignKey, Date , Boolean
from sqlalchemy.orm import relationship

from library_app.db.database import Base


class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_copy_id = Column(Integer, ForeignKey('book_copies.id'))
    borrower_id = Column(Integer, ForeignKey('borrowers.id'))
    #   # loan.due_date = date(2026, 7, 15)

    start_date = Column(Date(), nullable=False)
    due_date = Column(Date(), nullable=False)
    loan_closing_date = Column(Date(), nullable=True)
    is_active = Column(Boolean)


    bookCopy = relationship("BookCopy")
    borrower = relationship("Borrower")
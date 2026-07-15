
from datetime import datetime, timedelta  ,timezone
from sqlalchemy import select, func, desc

from library_app.models import  Book , Loan, BookCopy , BookCopyState


def check_single_book(db, book_id: int):

    available= False

    stmt = (
        select(

            Book,
            BookCopy.copy_state
        )
        .join(BookCopy, BookCopy.book_id == Book.id)
        .where(Book.id == book_id)
    )

    book = db.execute(stmt).scalars().first()

    if book is None:
        return book, available

    for copy in book.copies:
        available = True
        if copy.copy_state == BookCopyState.AVAILABLE:
            available = True
            break

    return book, available






def get_top_5_books(db, n_days_window: int = 7):
    date_threshold = datetime.now(timezone.utc)  - timedelta(days=n_days_window)

    stmt = (
        select(

            Book,
            func.count(Loan.id).label("book_loan_count")
        )
        .join(BookCopy, BookCopy.book_id == Book.id)#
        .join(Loan, Loan.book_copy_id == BookCopy.id)
        .where(Loan.start_date >= date_threshold)
        .group_by(Book.id)
        .order_by(desc("book_loan_count"))
        .limit(n_days_window)
    )

    results = db.execute(stmt).all()


    result_books = [
         row[0]

        for row in results
    ]


    return result_books



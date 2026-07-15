from datetime import date, timedelta

from library_app.models import BookCopy, BookCopyState, Loan, Borrower
from library_app.core.app_exceptions import NoAvailableBookCopy, LoanNotFound, ClientNotFound, PastDateException



def get_date_n_days_from_now(n_days,today_method):
    if n_days < 0:
        raise PastDateException("Can't generate a new date in the past")
    return today_method() + timedelta(days=n_days)




def get_current_loan(db, copy_id: int):
    return (
        db.query(Loan)
        .filter(
            Loan.book_copy_id == copy_id,
            Loan.is_active == True
        )
        .first()
    )
def is_copy_available(db, copy_id: int) -> bool:
    return not db.query(Loan).filter(
        Loan.book_copy_id == copy_id,
        Loan.is_active == True
    ).first()




def create_loan(db, client_id, book_id, days_to_be_borrowed = 7, today_method =date.today):

    borrower = (
        db.query(Borrower)
        .filter(Borrower.id == client_id)
        .first()
    )

    if borrower is None:
        raise ClientNotFound(f"No borrower found for the id {client_id}")


    copy = (
        db.query(BookCopy)
        .filter(
            BookCopy.book_id == book_id,
            BookCopy.copy_state == BookCopyState.AVAILABLE
        ).with_for_update() # avoids some issues with simultaneous requests
        .first()
    )

    if copy is None:
        raise NoAvailableBookCopy(f"No available copy found for book with id {book_id}")


    loan = Loan(
        borrower_id=client_id,
        book_copy_id=copy.id,
        start_date = date.today(),
        is_active=True,
        due_date=get_date_n_days_from_now(days_to_be_borrowed,today_method)

    )

    db.add(loan)

    copy.copy_state = BookCopyState.BORROWED
    db.flush()

    # db.commit()
    db.refresh(loan)

    return loan




def finish_loan(db, loan_id):

    loan = (
        db.query(Loan)
        .filter(
            Loan.id == loan_id,
            Loan.is_active == True
        )
        .first()
    )

    if loan is None:
        raise LoanNotFound()

    loan.is_active = False
    loan.bookCopy.copy_state = BookCopyState.AVAILABLE

    loan.loan_closing_date = date.today()

    db.flush()

    return loan



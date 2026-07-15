from library_app.models import  Borrower


def create_borrower(db, borrower_email:str, borrower_phone :str ):


    new_borrower = Borrower(
        email=borrower_email,
        phone=borrower_phone,
    )


    db.add(new_borrower)
    db.flush()

    db.refresh(new_borrower)

    return new_borrower


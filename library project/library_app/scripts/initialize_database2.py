from library_app.borrowers.borrower_service import create_borrower
from library_app.db.database import SessionLocal
from library_app.loans.loan_service import create_loan, finish_loan
from library_app.models import *




def add_loans():
    db = SessionLocal()

    borrower_names = ['Hannah','Stanley','Pablo','Fred','Louise','Liam']
    for i, borrower_name in enumerate(borrower_names):
        try:
            email = borrower_name+str(11*i)+'@email.com'
            phone = '00000000'+str(i)
            create_borrower(db, email, phone)
            db.commit()
        except Exception as e:
            print(f"An error occurred: {e}")



    clIDS = [2,2,3,4,
            1,3,4,2,
             5,2]
    bookIDS = [3,1,5,2,
               1,3,1,4,
               6,2 ]


    count = 0;
    for (client_id, book_id) in zip(clIDS, bookIDS):
        try:
            #   # loan.due_date = date(2026, 7, 15)

            create_loan(db, client_id, book_id)
            db.commit()
        except Exception as e:
            print(f"An error occurred starting loan {count }: {e} , book id {book_id}")

        if count >1  :
            try:
                loan_id = count-1
                finish_loan(db, loan_id)
            except Exception as e:
                print(f"An error occurred ending loan {count}: {e} , book id {book_id}")

        count += 1








if __name__ == "__main__":

    add_loans()


import datetime



from library_app.core.security import hash_password
from library_app.db.database import SessionLocal
from library_app.db.database import Base, engine
from library_app.models import *
from library_app.models.book_copies import BookCopyState

# from models import Book


def _add_employees( db):

    if db.query(Employee).first() is None:
        print("Adding employees...")
        print(Employee.__table__.columns.keys())
        employees = [
            Employee(first_name="John", last_name="A", is_active=True ,hire_date = datetime.date(1997, 5, 17)),
            Employee(first_name="Alice", last_name="B", is_active=True, hire_date = datetime.date(2001, 5, 1)),
            Employee(first_name="Bob", last_name="C", is_active=False, hire_date = datetime.date(2002, 1, 12)),
        ]
        passwords =['AAA', 'BBB', 'CCC']

        for  i, employee in enumerate(employees):
            account = EmployeeAccount(
                password_hash=hash_password(passwords[i])
            )
            employee.account = account



        db.add_all(employees)
        db.commit()









def _add_books_and_authors(db):
    if db.query(Book).first() is None:



        print("Adding books and authors...")
        authors = [
            Author(
                first_name= "Jane",
                last_name = "Jones",
                year_of_birth = 1965
            ) ,
            Author(
                first_name="Shirley",
                last_name="K",
                year_of_birth=1975
            ),

            Author(
                first_name="Maurice",
                last_name="H",
                year_of_birth=1987
            ),
            Author(
                first_name="Jolene",
                last_name="T",
                year_of_birth=1961
            ),

            Author(
                first_name="Brandon",
                last_name="W",
                year_of_birth=1987
            ),

            Author(
                first_name="Ulyses",
                last_name="Y",
                year_of_birth=1987
            ),
            Author(
                first_name="Anonymous"
            ),

        ]

        authors[0].written_books.append(
            Book(
                publication_year=1992,
                isbn='000-0-00-000000-0',
                title='The Blue Cat'

            )
        )
        authors[0].written_books.append(
            Book(
                publication_year=1994,
                isbn='111-1-11-111111-1',
                title='The Green Cat'

            )
        )

        authors[1].written_books.append(
            Book(
                publication_year=1971,
                isbn='222-2-22-000000-2',
                title='A History of the Roman Empire'

            )
        )


        authors[2].written_books.append(
            Book(
                publication_year=2002,
                isbn='333-3-33-000000-3',
                title='Learn Chinese in 3 months'

            )
        )


        authors[3].written_books.append(
            Book(
                publication_year=1998,
                isbn='444-4-44-444444-4',
                title='200 Knitting Patterns'

            )
        )


        authors[4].written_books.append(

            Book(
                publication_year=2006,
                isbn='555-5-55-555555-5',
                title='The Respiratory System'

            )
        )
        authors[4].written_books.append(
            Book(
                publication_year=2006,
                isbn='666-6-66-666666-6',
                title='The Nervous System'

            ),
        )

        authors[5].written_books.append(
            Book(
                publication_year=1982,
                isbn='777-7-77-777777-7',
                title='The Adventures of Mr. Jackson'

            )
        )
        authors[6].written_books.append(
            Book(
                publication_year=1881,
                isbn='888-8-88-888888-8',
                title='Tales of the grasslands'
            )
        )


        copy_count =0;
        for author in authors:
            for book in author.written_books:

                nCopies = 1 + (copy_count % 3)

                for _ in range(nCopies):
                    copy_count +=1
                    cState = BookCopyState.DAMAGED if copy_count % 6 == 5 else BookCopyState.AVAILABLE

                    book.copies.append(
                        BookCopy(
                            copy_state = cState
                        )

                    )





        db.add_all(authors)
        db.commit()







def init_db():
    # Base.metadata.create_all(bind=engine)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()


    _add_employees(db)
    _add_books_and_authors(db)



if __name__ == "__main__":
    print( "Starting database initialization...")
    init_db()










import pytest



from library_app.models import *
from library_app.models.book_copies import BookCopyState


from datetime import date


 



# preferably use flush so commits are surely not kept through different tests

@pytest.fixture(scope="function")
def borrower_fixture(db):
    borrower = Borrower ( email = "abc@xyz.com", phone = '111111111')

    
    db.add(borrower)
    db.flush()
    db.refresh(borrower)
    return borrower


@pytest.fixture(scope="function")
def author_fixture(db):



    
    author = Author(
                first_name= "Jane",
                last_name = "Jones",
                year_of_birth = 1965
            ) 
    

    db.add(author)
    db.flush()
    return author

@pytest.fixture(scope="function")
def book_fixture(db):




    book =          Book(
                publication_year=1992,
                isbn='000-0-00-000000-0',
                title='The Blue Cat'

            )
    

     
    db.add(book)
    db.flush()
    return book







@pytest.fixture(scope="function")
def book_with_writer_and_copy_fixture(db, book_fixture,author_fixture ):




        

    book_copy =   BookCopy( copy_state = BookCopyState.AVAILABLE )
    book_fixture.copies.append( book_copy)

    author_fixture.written_books.append(book_fixture)
    # db.add(book_copy)
    # no add since book 
    db.flush()
    return book_fixture




@pytest.fixture(scope="function")
def loan_fixture(db,book_with_writer_and_copy_fixture,borrower_fixture):
    
    copies =book_with_writer_and_copy_fixture.copies
    

    loan = Loan(
        borrower_id=borrower_fixture.id,
        book_copy_id=copies[0].id,
        start_date = date(2025, 2, 2),
        is_active=True,
        due_date= date(2025, 2, 9),

    )   
    db.add(loan)
    db.flush()
    return loan

 
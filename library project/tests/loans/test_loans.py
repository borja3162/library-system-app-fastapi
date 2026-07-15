
# from library_app.models import Book, BookCopy, Author,Loan
from library_app.loans.loan_service import create_loan
from library_app.db.database import Base


from datetime import date





import pytest



def mock_today():
    return date(2026, 7, 7)



@pytest.mark.unit
def test_create_loan(db,book_with_writer_and_copy_fixture , borrower_fixture):


    loan = create_loan(db , borrower_fixture.id, book_with_writer_and_copy_fixture.id,7,mock_today)
    assert loan is not None      # check 1
    assert loan.borrower_id == borrower_fixture.id
    assert loan.due_date == date(2026, 7, 14)

    
 




@pytest.mark.asyncio 
async def test_active_loans_endpoint(client ,valid_token_for_employee, loan_fixture):


    response = await client.get(
            "/loans/active?page=1",
        headers={
            "Authorization": f"Bearer {valid_token_for_employee}"
        }



        
    )

    assert response.status_code == 200

    
    resp_json=response.json()
    assert resp_json[0]['is_active']
    


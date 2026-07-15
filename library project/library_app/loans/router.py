
from fastapi import APIRouter, HTTPException
from starlette import status



from library_app.auth.dependencies import curent_employee
from library_app.core.pagination import order_and_paginate_query
from library_app.core.app_exceptions import NoAvailableBookCopy, LoanNotFound, ClientNotFound, PastDateException
from library_app.db.session import db_dependency
from library_app.loans.loan_service import create_loan
from library_app.loans.loan_service import  finish_loan as finish_loan_service
from library_app.models import Loan , EmployeeAccount
from library_app.schemas.loans import LoanResponse








router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("/active" , status_code=status.HTTP_200_OK,  response_model=list[LoanResponse])
async def get_active_loans(db: db_dependency , emp: curent_employee , page:int ):

    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    results = db.query(Loan).filter(Loan.is_active.is_( True))
    results = order_and_paginate_query(results,Loan.id,page)


    return results.all()

@router.post("/create" , status_code=status.HTTP_201_CREATED , response_model=LoanResponse)
async def create_new_loan(db: db_dependency , emp: curent_employee ,
                           client_id:int , book_id:int , days_to_be_borrowed:int ):

    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    try:
        result = create_loan(db, client_id, book_id, days_to_be_borrowed)
        db.commit()
    except ClientNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoAvailableBookCopy as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except PastDateException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return result




@router.patch("/finish/{loan_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def finish_loan(db: db_dependency , emp: curent_employee ,
                           loan_id: int ):

    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    try:
        finish_loan_service(db, loan_id)
        db.commit()
    except LoanNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))




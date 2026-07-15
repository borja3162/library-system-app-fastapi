

from fastapi import APIRouter, HTTPException
from starlette import status


from library_app.auth.dependencies import curent_employee
from library_app.borrowers.borrower_service import create_borrower
from library_app.db.session import db_dependency
from library_app.models import Borrower , EmployeeAccount
from library_app.schemas.borrowers import BorrowerRequest , BorrowerResponse



router = APIRouter(prefix="/borrowers", tags=["borrowers"])


@router.get("/{borrower_id}" , status_code=status.HTTP_200_OK , response_model= BorrowerResponse)
async def get_borrower_by_id(db: db_dependency , emp: curent_employee , borrower_id: int):

    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    result = db.query(Borrower).filter(Borrower.id == borrower_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return result



@router.post("/create" , status_code=status.HTTP_200_OK,response_model= BorrowerResponse)
async def create_new_borrower_profile(db: db_dependency , emp: curent_employee , borrower: BorrowerRequest):
                              # borrower_email:str, borrower_phone :str):

    if emp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")



    result = create_borrower(db, borrower.email, borrower.phone )
    db.commit()

    return result





from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from library_app.auth.auth_service import authenticate_employee
from library_app.core.security import create_access_token
from library_app.db.session import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    try:
        user_id = int(form_data.username)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid employee ID format")

    employee = authenticate_employee(
        db,
        employee_id = user_id,
        password = form_data.password
    )

    if not employee:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    token = create_access_token({"sub": str (employee.id) })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

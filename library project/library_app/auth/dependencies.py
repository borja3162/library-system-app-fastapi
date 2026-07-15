from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Annotated

from library_app.core.security import decode_token
from library_app.db.session import get_db
from library_app.models.employee_accounts import EmployeeAccount





# jwt Bearer token is extracted and passed into dependency function
# url is used for authomatic swagger docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")





def get_current_employee(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)

        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


    employee_id = int(username)
    account_info = db.query(EmployeeAccount).filter(  EmployeeAccount.employee_id == employee_id  ) .first()
    if not account_info:
        raise HTTPException(status_code=401, detail="User not found")

    return account_info


curent_employee = Annotated[ EmployeeAccount,    Depends(get_current_employee) ]

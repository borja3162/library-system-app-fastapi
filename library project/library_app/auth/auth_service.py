from sqlalchemy.orm import Session

from library_app.core.security import create_access_token , decode_token , verify_password
from library_app.models.employee_accounts import EmployeeAccount


def authenticate_employee(db: Session, employee_id: int, password: str):

    account_info = db.query(EmployeeAccount).filter(  EmployeeAccount.employee_id == employee_id  ) .first()

    if not account_info:
        return None
    if not verify_password(password, account_info.password_hash):
        return None
    return account_info






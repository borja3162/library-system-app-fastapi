
from  datetime import date
from pydantic import BaseModel ,ConfigDict


class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_copy_id : int
    borrower_id : int
    start_date : date
    due_date : date
    loan_closing_date : date | None
    is_active : bool





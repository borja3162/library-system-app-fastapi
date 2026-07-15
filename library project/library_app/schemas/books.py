
from pydantic import BaseModel ,ConfigDict




class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    isbn: str
    publication_year: int


class BookWithAvailabilityResponse(BookResponse):
    is_available: bool = False










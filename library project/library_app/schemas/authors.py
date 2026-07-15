from pydantic import BaseModel ,ConfigDict




class AuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str | None
    year_of_birth: int | None = None





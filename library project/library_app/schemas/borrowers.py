from pydantic import BaseModel ,ConfigDict  , field_validator

import re




# ^ string start
# [A-Za-z0-9_.] letters, numbers or _ or . . Points within brackets behave as simple character
# + at least one
# \.  point character (when outside brackets)
# $ end of string
EMAIL_REGEX_MATCHING_STR= r"^[A-Za-z0-9._]+@[A-Za-z0-9]+\.[A-Za-z]+$"
EMAIL_RE = re.compile(EMAIL_REGEX_MATCHING_STR )



# ^ string start
# \+ plus character, different from + (at least one)
# ? optional (at most 1)
# {n,m} from n to m repetitions of specified pattern: {8,}   at least 8 times
# $ end of string
PHONE_REGEX_MATCHING_STR= r"^\+?[0-9]{8,}$"
PHONE_RE = re.compile(PHONE_REGEX_MATCHING_STR )



class BorrowerRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:



        #str.maketrans() builds a correspondence of what character goes to what character
        # third argument: what characters will be deleted
        normalized = value.translate(str.maketrans("", "", " -()."))

        if not PHONE_RE.fullmatch(normalized):
            raise ValueError("Invalid phone number")

        return value  # or return normalized


    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:

        if not EMAIL_RE.fullmatch(value):
            raise ValueError("Invalid email")

        return value  # or return normalized



class BorrowerResponse(BorrowerRequest):
    id:int
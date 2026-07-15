

import pytest
from library_app.core.security import decode_token
# from jwt import InvalidTokenError, ExpiredSignatureError
from jose.exceptions import ExpiredSignatureError, JWTError




@pytest.mark.unit
def test_valid_token(valid_token_no_employee ):



    payload = decode_token(valid_token_no_employee)
    assert payload is not None

 
 

@pytest.mark.unit
def test_invalid_token(invalid_token ):

    result = None
    try:
        result = decode_token(invalid_token)
    except JWTError:
        pass

    assert result is None
 

 

@pytest.mark.unit
def test_expired_token(expired_token ):

    result = None
    try:
        result = decode_token(expired_token)
    except ExpiredSignatureError:
        pass

    assert result is None

 

 
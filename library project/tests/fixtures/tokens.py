import pytest
from library_app.core.security import create_access_token


from library_app.models.employees import Employee
from library_app.models.employee_accounts import EmployeeAccount
from library_app.core.security import hash_password



# from library_app.models import *
from datetime import date









@pytest.fixture(scope="function")
def employee_with_account_fixture(db):
    employee= Employee(first_name="John", last_name="A", is_active=True ,hire_date = date(1997, 5, 17))
    account = EmployeeAccount(
                password_hash=hash_password('AAA')
            )
    employee.account = account
    
    db.add(employee)
    db.flush()
    # db.refresh(employee)

    

    return employee





@pytest.fixture(scope="function")
def valid_token_no_employee():
    
    token = create_access_token({"sub": "ABC"})
    
    return token





@pytest.fixture(scope="function")
def valid_token_for_employee(employee_with_account_fixture):
    
    token = create_access_token({"sub": str(employee_with_account_fixture.id)})
    

    
    return token





@pytest.fixture(scope="function")
def invalid_token( valid_token_no_employee):
    
    first_char = 'a' if valid_token_no_employee[0] != 'a' else 'b'

    return first_char + valid_token_no_employee[1:] 




@pytest.fixture(scope="function")
def expired_token():
    token = create_access_token({"sub": "ABC"},minutes_to_expire = -5)
    
    return token





 
from library_app.models.employees import Employee

import pytest



TEST_NAME = "John"
TEST_IS_ACTIVE = True

@pytest.mark.unit
def test_create_employee(db):
    employee = Employee( first_name=TEST_NAME, last_name= "A", is_active = TEST_IS_ACTIVE)


    db.add(employee)
    # db.commit()
    db.flush()
    db.refresh(employee)

    assert employee.id is not None
    assert employee.first_name == "John"
    assert employee.is_active == TEST_IS_ACTIVE


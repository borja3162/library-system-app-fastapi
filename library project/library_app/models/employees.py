
from sqlalchemy import Column,Integer,String,Boolean , Date
from sqlalchemy.orm import relationship

from library_app.db.database import Base





class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # employee_id = Column(String, unique=True)
    hire_date = Column(Date)
    is_active = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)

    # this does not store "account" on employees table
    account = relationship(
            "EmployeeAccount", # ORM class
            back_populates="employee", # relationship inside ORM class
            uselist=False # for one to one relationship, returns an element instead of a list
        )
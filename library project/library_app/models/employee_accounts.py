
from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship

from library_app.db.database import Base



class EmployeeAccount(Base):
    __tablename__ = "employee_accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id =Column(
        ForeignKey("employees.id"),
        nullable=False
    )
    password_hash = Column(String)

    employee = relationship(
        "Employee",
        back_populates="account"
    )
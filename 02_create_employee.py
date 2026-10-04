from fastapi import APIRouter
from data_store import employees
from models import Employee

router = APIRouter()

@router.post("/employee")
def create_employee(employee: Employee):
    # Generate a new ID for the employee
    new_employee = employee.model_dump()
    employees.append(new_employee)
    return {"message": "Employee created successfully", "employee": new_employee}

from fastapi import APIRouter, FastAPI
from data_store import employees

router =APIRouter()

@router.get("/employees")
def get_employees():
    return employees

@router.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employee = next((emp for emp in employees if emp["id"] == employee_id), None)
    if employee:
        return employee
    else:
        return {"error": "Employee not found"}
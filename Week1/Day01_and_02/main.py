from importlib import import_module

from fastapi import FastAPI

get_invoices_routes = import_module("01_get_invoices").router
create_invoice_routes = import_module("02_create_invoice").router
get_employees_routes = import_module("01_get_employees").router
create_employee_routes = import_module("02_create_employee").router

app = FastAPI()

app.include_router(get_invoices_routes)
app.include_router(create_invoice_routes)
app.include_router(get_employees_routes)
app.include_router(create_employee_routes)
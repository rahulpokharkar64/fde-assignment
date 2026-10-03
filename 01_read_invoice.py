# 📌 Home Assignment – Read Invoice CSV
# Hi Team,
# Please use the shared homework_invoices.csv file and complete the following task.
#-------------------------------------------

# 1. Create a Python program named:
#    01_read_invoice.py
# 2. Read all invoice records from the given CSV file using Python.
# 3. For each invoice, read and check the following details:
#    - Vendor
#    - Amount
#    - Status
import csv

with open('data/homework_invoices.csv', 'r') as file:
    reader = csv.DictReader(file)
    invoices = list(reader)
    for invoice in invoices:
        vendor = invoice['vendor']
        amount = invoice['amount']
        status = invoice['status']
        print(f"Vendor: {vendor}, Amount: {amount}, Status: {status}")


# 4. Check the invoice amount:
#    - Identify invoices where the amount is greater than 100,000.
#    - Identify missing or invalid amount values.
# 5. Use try / except to handle invalid amount values so that the program continues processing the remaining records.
# 6. Print a simple summary at the end:
#    - Total invoices read
#    - Number of invoices greater than 100,000
#    - Number of invoices with missing/invalid amount

# Expected Flow:
# Read CSV → Read Each Invoice → Check Amount → Handle Invalid Data → Print Summary

with open('data/homework_invoices.csv', 'r') as file:
    reader = csv.DictReader(file)
    invoices = list(reader)
    total_invoices = len(invoices)
    invoices_greater_than_100k = 0
    invalid_amounts = 0

    for invoice in invoices:
        amount_str = invoice['amount']
        try:
            amount = float(amount_str)
            if amount > 100000:
                invoices_greater_than_100k += 1
        except ValueError:
            invalid_amounts += 1

print(f"Total invoices read: {total_invoices}")
print(f"Invoices greater than 100,000: {invoices_greater_than_100k}")
print(f"Invoices with missing/invalid amount: {invalid_amounts}")


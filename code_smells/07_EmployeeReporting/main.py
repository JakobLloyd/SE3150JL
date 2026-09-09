from pathlib import Path

from employee_report import EmployeeReport
from employee_table import EmployeeTable


data_file = Path(__file__).with_name("employees.enc")
table = EmployeeTable(data_file)

report = EmployeeReport(table)

manager_user = {
    "name": "Ana Martinez",
    "role": "manager",
    "department": "Sales",
}

print(f"User: {manager_user['name']}")
print(f"Role: {manager_user['role']}")
print("\nEmployees visible to this user:")
print(report.employee_list(manager_user))

print("\nGet employee E1003:")
print(report.get_employee("E1003", manager_user))

print("\n" + "=" * 50 + "\n")

hr_user = {
    "name": "Divya Patel",
    "role": "hr",
    "department": "Human Resources",
}

print(f"User: {hr_user['name']}")
print(f"Role: {hr_user['role']}")
print("\nEmployees visible to this user:")
print(report.employee_list(hr_user))

print("\nGet employee E1005:")
print(report.get_employee("E1005", hr_user))

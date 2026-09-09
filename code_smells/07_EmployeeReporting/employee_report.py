class EmployeeReport:
    def __init__(self, employee_table):
        self.employee_table = employee_table

    def employee_list(self, current_user):
        self._require_report_access(current_user)
        rows = self.employee_table.rows_for(current_user)
        return "\n".join(
            f"{row['employee_id']}: {row['name']} "
            f"({row['job_title']}, {row['department']})"
            for row in rows
        )

    def get_employee(self, employee_id, current_user):
        self._require_report_access(current_user)
        row = self.employee_table.employee_for(employee_id, current_user)
        return (
            f"ID: {row['employee_id']}\n"
            f"Name: {row['name']}\n"
            f"Department: {row['department']}\n"
            f"Title: {row['job_title']}\n"
            f"Salary: ${row['salary']:,}"
        )

    def _require_report_access(self, current_user):
        if current_user["role"] not in {"manager", "hr"}:
            raise PermissionError("Reports require manager or HR access")

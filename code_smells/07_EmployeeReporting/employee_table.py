import json

from cryptography.fernet import Fernet


ENCRYPTION_KEY = b"8o4N1Mz4Ozzhxi-uVjzzda_d6UeKGiIBFQbhljI9rQo="


class EmployeeTable:
    def __init__(self, filename):
        encrypted_data = filename.read_bytes()
        decrypted_data = Fernet(ENCRYPTION_KEY).decrypt(encrypted_data)
        self._rows = json.loads(decrypted_data.decode("utf-8"))

    def rows_for(self, current_user):
        if current_user["role"] == "hr":
            return [dict(row) for row in self._rows]

        if current_user["role"] != "manager":
            raise PermissionError("Employee records require manager or HR access")

        return [
            dict(row)
            for row in self._rows
            if row["department"] == current_user["department"]
        ]

    def employee_for(self, employee_id, current_user):
        for row in self.rows_for(current_user):
            if row["employee_id"] == employee_id:
                return row

        raise PermissionError("Employee is not visible to this user")

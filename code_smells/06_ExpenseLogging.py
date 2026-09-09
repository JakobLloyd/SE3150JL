"""
The company uses this application to manage employee expenses.

Requirements:

- Ask employees to enter expense information.
- Validate expenses using company policy.
- Calculate reimbursements.
- Store approved expenses in the database.
- Display confirmation to the employee.
- Generate reports for accounting.
- Format notification emails.

"""

import sqlite3
from datetime import datetime


class ExpenseApplication:
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")

        self.connection.execute("""
            create table expenses(
                employee text,
                category text,
                amount real,
                reimbursement real,
                submitted text
            )
        """)

    def read_expense(self):
        employee = input("Employee name: ")
        category = input("Expense category (mileage, meal, hotel, supplies or other): ")
        amount = float(input("Amount: $"))

        return employee, category, amount

    def validate_expense(self, category, amount):
        if amount <= 0:
            return False

        if category == "meal" and amount > 75:
            return False

        if category == "hotel" and amount > 250:
            return False

        if category not in {
            "meal",
            "hotel",
            "mileage",
            "supplies",
            "other"
        }:
            return False

        return True

    def calculate_reimbursement(self, category, amount):
        if category == "mileage":
            return amount * 0.67

        if category == "meal":
            return min(amount, 75)

        if category == "hotel":
            return min(amount, 250)

        return amount

    def save_expense(
        self,
        employee,
        category,
        amount,
        reimbursement,
    ):
        self.connection.execute(
            """
            insert into expenses
            values (?, ?, ?, ?, ?)
            """,
            (
                employee,
                category,
                amount,
                reimbursement,
                datetime.now().isoformat(),
            ),
        )

        self.connection.commit()

    def draw_confirmation_screen(
        self,
        employee,
        reimbursement,
    ):
        print("+--------------------------------+")
        print(f" Employee: {employee}")
        print(f" Reimbursement: ${reimbursement:.2f}")
        print("+--------------------------------+")

    def create_accounting_report(self):
        rows = self.connection.execute(
            """
            select category, sum(reimbursement)
            from expenses
            group by category
            """
        )

        report = ["MONTHLY EXPENSE REPORT"]

        for category, total in rows:
            report.append(
                f"{category.title()}: ${total:.2f}"
            )

        return "\n".join(report)

    def format_email(
        self,
        employee,
        reimbursement,
    ):
        return (
            f"To: {employee}\n"
            f"Subject: Expense approved\n\n"
            f"Your reimbursement of "
            f"${reimbursement:.2f} was approved."
        )

    def run(self):
        employee, category, amount = (
            self.read_expense()
        )

        if not self.validate_expense(
            category,
            amount,
        ):
            print("Expense rejected.")
            return

        reimbursement = (
            self.calculate_reimbursement(
                category,
                amount,
            )
        )

        self.save_expense(
            employee,
            category,
            amount,
            reimbursement,
        )

        self.draw_confirmation_screen(
            employee,
            reimbursement,
        )

        print()
        print(self.format_email(
            employee,
            reimbursement,
        ))


if __name__ == "__main__":
    ExpenseApplication().run()
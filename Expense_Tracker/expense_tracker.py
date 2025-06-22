from expense import Expense
from weekly_expense import Weekly_Expense

class Expense_Tracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            print("Expense removed successfully.") # Stylise to have the name printed
        else:
            print("Invalid expense index.")

    def list_expense(self):
        if(len(self.expenses) == 0):
            print("No expenses found.")
        else:
            print("Expense List:")
            for i, expense in enumerate(self.expenses, start = 1):
                print(f"{i}. Name: {expense.name}")

    def summarise_expenses(self):
        if (len(self.expenses) == 0):
            print("No expenses found.")
        else:
            print("Expense List:")
            for i, expense in enumerate(self.expenses, start = 1):
                current_budget = sum(weekly_expense for weekly_expense in expense.weekly_expenses)
                print(f"{i}. Name: {expense.name}, Amount: {expense.amount:.2f}, Count: {len(expense.weekly_expenses)}, Current budget: {current_budget:.2f}")

    def total_expenses(self):
        total = sum(expense.amount for expense in self.expenses)
        print(f"Total Expenses: ${total:.2f}")


from weekly_expense import Weekly_Expense

class Expense:
    def __init__(self, name, amount, start_date, frequency, interval):
        self.weekly_expenses = []

        self.name = name
        self.amount = amount
        self.start_date = start_date
        self.frequency = frequency
        self.interval = interval

    def __str__(self):
        return f"\nName: {self.name}\nAmount: ${self.amount}\nStart Date: {self.start_date}\nFrequency: {self.frequency}\nInterval: {self.interval}"

    def add_weekly_expense(self, weekly_expense):
        self.weekly_expenses.append(weekly_expense)

    def remove_weekly_expense(self, index):
        if 0 <= index < len(self.weekly_expenses):
            del self.weekly_expenses[index]
        else:
            print("Invalid weekly expense index")
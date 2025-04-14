from expense import Expense
from weekly_expense import Weekly_Expense

def main():
    tracker = Expense_Tracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. List Expenses")
        print("4. Summarise Expenses")
        print("5. Total Expenses")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            while True:
                try:
                    name = input("Enter the name: ")
                    amount = float(input("Enter the amount (in number digits): "))
                    start_date = input("Enter the date (YYYY-MM-DD): ")
                    frequency = input("Enter the frequency: ")
                    interval = input("Enter the interval: ")

                    expense = Expense(name, amount, start_date, frequency, interval)
                    tracker.add_expense(expense)
                    print("Expense added successfully.")
                    break
                except ValueError:
                    print("Please enter the correct value.")
        elif choice == "2":
            index = int(input("Enter the expense index to remove: ")) - 1
            tracker.remove_expense(index)
        elif choice == "3":
            tracker.list_expense()
        elif choice == "4":
            tracker.summarise_expenses()
        elif choice == "5":
            tracker.total_expenses()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
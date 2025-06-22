from expense_tracker import Expense_Tracker
from expense import Expense
from weekly_expense import Weekly_Expense

def view_expense(expense: Expense) -> None:
    print(expense)
    #while True:
        #print("\nExpense Menu:")
        #print("1. Add Weekly Expense")
        #print("2. Remove Weekly Expense")

        #choice_EMenu = input("Enter your choice (1-): ")



def main():
    tracker = Expense_Tracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. Remove Expense")
        print("3. View Expense")
        print("4. Summarise Expenses")
        print("5. Total Expenses")
        print("6. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            while True:
                try:
                    name = input("Enter the name: ")
                    amount = float(input("Enter the amount (in digits): "))
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
            if len(tracker.expenses) == 0:
                print("No expenses found.")
            else:
                try:
                    index = int(input("Enter the expense index to view: ")) - 1
                    view_expense(tracker.expenses[index])
                except* ValueError:
                    print("Please enter the correct value.")
                except* IndexError:
                    print("Expense not found.")
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
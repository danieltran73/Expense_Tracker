import sqlite3

"""Smaller functions"""

# Frequency to week ratio converter
def convert_frequency(frequency: str) -> int:
    match frequency:
        case "weekly":
            return 1
        case "bi-weekly":
            return 2
        case "monthly":
            return 4
        case "yearly":
            return 52
        case _:
            raise ValueError(f"Unsupported frequency: {frequency}")
        

"""Database functions"""
# Initialize database
def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
         print(f"Error: {e}")
         raise
    

# Create a table in the db
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        frequency TEXT NOT NULL,
        week_ratio INTEGER,
        counter INT DEFAULT 0)
    """
    try:
        with connection:
            connection.execute(query)
        print("Table was created!")
    except Exception as e:
        print(e)

# Add expense
def insert_expense(connection, name: str, price: float, frequency: str, week_ratio: int) -> None:
    query = "INSERT INTO expenses (name, price, frequency, week_ratio) VALUES (?, ?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (name, price, frequency, week_ratio))
        print(f"Expense: {name} was added to your database!")
    except Exception as e:
        print(e)

# View all expenses
def fetch_expenses(connection, condition: str = None) -> list[tuple]: #(Rent, 520, frequency)
    query = "SELECT id, name, price, frequency, counter FROM expenses"
    if condition:
        query += f" WHERE {condition}"

    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(e)

# Delete expense
def delete_expense(connection, expense_id:int):
    query = "DELETE FROM expenses WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (expense_id,))
        print(f"\nEXPENSE ID: {expense_id} was deleted!")
    except Exception as e:
        print(e)

# Total budget
def total_expense(connection) -> str:
    query = "SELECT SUM((CAST(price AS REAL) / CAST(week_ratio AS REAL)) * counter) FROM expenses"
    try:
        with connection:
            total = connection.execute(query).fetchone()[0]
        return total
    except Exception as e:
        print(e)

# Increment counters
"""
- Alter all counter by one with a confirming message and 
quick list of expenses and their counter
"""

def increment_one_counter(connection, expense_id:int) -> None: 
    query = "UPDATE expenses SET counter = counter + 1 WHERE id = ?"

    try:
        with connection:
            connection.execute(query, (expense_id,))
        print("\nCounter is incremented by 1.")
    except Exception as e:
        print(e)

def increment_all_counters(connection) -> None:
    query = "UPDATE expenses SET counter = counter + 1"

    try:
        with connection:
            connection.execute(query)
        print("\nAll counters are incremented by 1.")
    except Exception as e:
        print(e)

# Decrement counters

def pay_expense(connection, expense_id:int) -> None:
    query_1 = "SELECT SUM((CAST(price AS REAL) / CAST(week_ratio AS REAL)) * counter) FROM expenses WHERE id = ?"
    query_2 = "UPDATE expenses SET counter = 0 WHERE id = ?"
    try:
        with connection:
            bill = connection.execute(query_1, (expense_id,)).fetchone()[0]
            print(f"\n${bill} has been paid for expense id {expense_id}.")
            connection.execute(query_2, (expense_id,))
    except Exception as e:
        print(e)

# Main Function
def main():
    connection = get_connection("expense_tracker.db")

    try:
        # Create the table
        create_table(connection)

        while True:
            start_input = input("\nEnter your choice (Add, Delete, View, Increment, Pay, Total, Exit): ").lower()
            if start_input == 'add':
                while True:
                    try:
                        name = input("Enter expense name: ")
                        price = float(input("Enter price: $"))
                        frequency = input("Enter frequency (Weekly/Bi-Weekly/Monthly/Yearly): ").lower()

                        if frequency not in {"weekly", "bi-weekly", "monthly", "yearly"}:
                            print("Please enter the correct format!")
                            break

                        week_ratio = convert_frequency(frequency)

                        insert_expense(connection, name, price, frequency, week_ratio)
                        break
                    except ValueError:
                        print("Please enter the correct value!")
            
            elif start_input == "view":
                print("All Expenses:")
                for expense in fetch_expenses(connection):
                    print(expense)

            elif start_input == "delete":
                expense_id = int(input("Enter expense id: "))
                delete_expense(connection, expense_id)

            elif start_input == "increment":
                choice_input = input("Whould you like to increment 'one' or 'all' expenses?: ").lower()
                match choice_input:
                    case "one":
                        id_input = int(input("Enter expense id: "))
                        increment_one_counter(connection, id_input)
                    case "all":
                        increment_all_counters(connection)
                        total_expense(connection)
                    case _:
                        raise ValueError(f"Unsupported choice: {choice_input}")
                        break
                        
                for expense in fetch_expenses(connection):
                    print(expense)

            elif start_input == "pay":
                expense_id = int(input("Enter expense id: "))
                pay_expense(connection, expense_id)
                
                print(f"Current total budget: ${total_expense(connection):.2f}")

            elif start_input == "total":
                total = total_expense(connection)
                if total is not None:
                    print(f"Total budget: ${total:.2f}")
                else:
                    print("No expenses found.")

            elif start_input == "exit":
                break
            
            else:
                print("Invalid choice! Please try again.")
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
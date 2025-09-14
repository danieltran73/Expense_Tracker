import sqlite3
import logging
import os
import csv
from datetime import datetime

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
        

"""Logging/Data recording functions"""

# # Check if the log folder exists, if not create it
# def check_log_folder() -> str:
#     log_folder = "logs"
#     if not os.path.exists(log_folder):
#         os.makedirs(log_folder)
#         print(f"Log folder '{log_folder}' created.")
#     return log_folder

# Check if the year folder exists, if not create it
def check_year_folder(year: int) -> None:
    year_folder = os.path.join("logs", str(year))
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
        print(f"Year folder '{year}' created in logs.")
    return None

# Check if the text folder exists, if not create it
def check_text_folder(year: int) -> str:
    text_folder = os.path.join("logs", str(year), "text_files")
    if not os.path.exists(text_folder):
        os.makedirs(text_folder)
        print(f"Text folder '{text_folder}' created in logs/{year}.")
    return text_folder

# Check if the csv file exists, if not create it
def check_csv_file(year: int) -> str:
    csv_file = os.path.join("logs", str(year), f"expenses-{year}.csv")
    if not os.path.exists(csv_file):
        check_year_folder(year)
        with open(csv_file, 'w') as csv_file:
            fieldnames = ['Date', 'Day_of_the_week', 'Changed_object', 'Change_type', 
                          'Changed_amount', 'Current_total', 'Message']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            print(f"CSV file '{csv_file}' created with headers.")
    return csv_file

# Write csv lines
def write_csv_line(changed_object: str, changed_type: str, 
                   changed_amount: float, current_total: float, message: str) -> None:
    try:
        today = datetime.now()
        csv_file = check_csv_file(today.strftime("%Y"))
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([today.strftime("%Y/%m/%d"), today.strftime("%A"), changed_object, 
                             changed_type, f"${changed_amount:.2f}", f"${current_total:.2f}", message])
        print(f"CSV line written: {today.strftime('%Y/%m/%d')} - {changed_object} - {changed_type} - ${changed_amount:.2f}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
    return None

# Write weekly summary text files with title from starting date to ending date of the current week

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
def increment_one_counter(connection, expense_id:int) -> None: 
    query_1 = "UPDATE expenses SET counter = counter + 1 WHERE id = ?"
    query_2 = "SELECT name, (CAST(price AS REAL) / CAST(week_ratio AS REAL)), ((CAST(price AS REAL) / CAST(week_ratio AS REAL)) * counter) FROM expenses WHERE id = ?"

    try:
        with connection:
            connection.execute(query_1, (expense_id,))
            selection = connection.execute(query_2, (expense_id,))
            name = selection.fetchone()[0]
            amount = selection.fetchone()[1]
            total = selection.fetchone()[2]
        print(f"\nCounter {name} is incremented by 1.")
        logging.info(f"Counter {name} is incremented by 1.")
        write_csv_line(name, "Single Increment", amount, total, "Counter {name} is incremented by 1.")
    except Exception as e:
        print(e)

def increment_all_counters(connection) -> None:
    query = "UPDATE expenses SET counter = counter + 1"

    try:
        with connection:
            connection.execute(query)
        total = total_expense(connection)
        print(f"\nAll counters are incremented by 1.\nTotal budget: ${total:.2f}")
        logging.info(f"\nAll counters are incremented by 1. Total budget: ${total:.2f}")
    except Exception as e:
        print(e)

# Decrement counters

def pay_expense(connection, expense_id:int) -> None:
    query_1 = "SELECT name, counter, SUM((CAST(price AS REAL) / CAST(week_ratio AS REAL)) * counter) FROM expenses WHERE id = ?"
    query_2 = "UPDATE expenses SET counter = 0 WHERE id = ?"
    try:
        with connection:
            name = connection.execute(query_1, (expense_id,)).fetchone()[0]
            counter = connection.execute(query_1, (expense_id,)).fetchone()[1]
            bill = connection.execute(query_1, (expense_id,)).fetchone()[2]
            print(f"\n${bill} has been paid for {name}")
            connection.execute(query_2, (expense_id,))
        logging.info(f"${bill} has been paid for {name}. Counter change from {counter} to 0.")
    except Exception as e:
        print(e)

# Main Function
def main():
    # Initialise logging
    logging.basicConfig(filename='weekly_logs.log',
                        format='%(asctime)s: %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logging.INFO,)

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
                while True:
                    try:
                        choice_input = input("Would you like to increment 'one' or 'all' expenses?: ").lower()
                        match choice_input:
                            case "one":
                                id_input = int(input("Enter expense id: "))
                                increment_one_counter(connection, id_input)
                            case "all":
                                increment_all_counters(connection)
                                total_expense(connection)
                            case _:
                                raise ValueError
                        
                        for expense in fetch_expenses(connection):
                            print(expense)
                        break
                    except ValueError:
                        print("Invalid choice! Please enter either 'one' or 'all'.")
                
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
import sqlite3

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
        id
        name
        price)
    """

# Main Function
def main():
    connection = get_connection("expense_tracker.db")

if __name__ == "__main__":
    main()
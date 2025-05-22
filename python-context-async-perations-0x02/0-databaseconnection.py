import sqlite3

class DatabaseConnection:
    """Context manager for handling SQLite database connections."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Opens a database connection and returns it."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensures the connection is closed, even if an error occurs."""
        if self.conn:
            self.conn.close()

# Using the context manager to fetch users
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)  # Print query results
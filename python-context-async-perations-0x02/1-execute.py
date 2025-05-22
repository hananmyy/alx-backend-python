import sqlite3

class ExecuteQuery:
    """Context manager for executing queries with automatic connection handling."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None

    def __enter__(self):
        """Opens database connection and executes the query."""
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        return cursor.fetchall()  # Return query results

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes connection, ensuring cleanup."""
        if self.conn:
            self.conn.close()

# Using the context manager to execute a query
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    
    with ExecuteQuery("users.db", query, param) as results:
        print(results)  # Print query results
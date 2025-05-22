import sqlite3
import functools
from datetime import datetime  # Required for timestamp

# Decorator to log SQL queries with timestamps
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0]  # Extract SQL query
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
        print(f"[{timestamp}] Executing Query: {query}")  # Log with timestamp
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users("SELECT * FROM users")
    print(users)
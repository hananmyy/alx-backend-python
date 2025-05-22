import time
import sqlite3
import functools

# Decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Connect to database
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to function
        finally:
            conn.close()  # Ensure connection is closed
        return result
    return wrapper

# Decorator to retry failed operations
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)  # Try executing function
                except sqlite3.OperationalError as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)  # Wait before retrying
            raise Exception("Max retries reached. Operation failed.")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
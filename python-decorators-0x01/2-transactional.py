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

# Decorator for transaction management
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Execute function
            conn.commit()  # Commit changes if successful
        except Exception as e:
            conn.rollback()  # Rollback if an error occurs
            print(f"Transaction failed: {e}")
            raise
        return result
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='new.email@example.com')
    print("Email updated successfully!")
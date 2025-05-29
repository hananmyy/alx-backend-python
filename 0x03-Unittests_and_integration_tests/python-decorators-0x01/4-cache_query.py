import sqlite3
import functools

# Cache dictionary to store query results
query_cache = {}

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

# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[1]  # Extract SQL query (second argument)
        if query in query_cache:  # Check if query is cached
            print(f"Using cached result for query: {query}")
            return query_cache[query]  # Return cached result
        
        result = func(*args, **kwargs)  # Execute query
        query_cache[query] = result  # Store result in cache
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Fetch users with caching
if __name__ == "__main__":
    users = fetch_users_with_cache("SELECT * FROM users")  # First call (executes query)
    users_again = fetch_users_with_cache("SELECT * FROM users")  # Second call (uses cache)
    print(users_again)
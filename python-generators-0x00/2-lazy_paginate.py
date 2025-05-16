import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

# Function to fetch paginated users (helper function)
def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        connection.close()
        return rows
    return []

# Generator function for lazy pagination
def lazy_paginate(page_size):
    offset = 0
    while True:
        users = paginate_users(page_size, offset)
        if not users:  # Stop iteration when no more data
            break
        yield users  # Yield the current page of users
        offset += page_size  # Move to the next page

# Example usage
if __name__ == "__main__":
    for page in lazy_paginate(100):  # Fetch users in pages of 100
        for user in page:
            print(user)  # Print each user lazily
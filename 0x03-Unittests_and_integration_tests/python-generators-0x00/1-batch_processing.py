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

# Generator function to stream users in batches
def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset};")
            rows = cursor.fetchall()

            if not rows:  # If no more rows, stop iteration
                break

            yield rows  # Yield batch of rows
            offset += batch_size

        cursor.close()
        connection.close()

# Function to process each batch (filtering users over age 25)
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        processed_batch = [user for user in batch if user["age"] > 25]
        for user in processed_batch:
            print(user)  # Print filtered users

# Example usage
if __name__ == "__main__":
    batch_processing(50)  # Process users in batches of 50
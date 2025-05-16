import mysql.connector
import os
import csv
from dotenv import load_dotenv

csv_file = os.path.join(os.getcwd(), "user_data.csv")  # Ensure correct CSV path

load_dotenv()

# Get credentials from .env file
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Create the ALX_prodev database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
        print("Database ALX_prodev created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

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

# Create user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

# Insert data from CSV into the table
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    name = VALUES(name), email = VALUES(email), age = VALUES(age);
                """, row)
        connection.commit()
        cursor.close()
        print(f"Data from {csv_file} inserted successfully.")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found. Ensure it's in the correct directory.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")

# Main execution
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data(conn, csv_file)
        conn.close()
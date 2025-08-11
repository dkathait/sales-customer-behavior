import os
import pandas as pd
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from test_gsheet import read_google_sheet

# Load environment variables
load_dotenv()

def load_data_to_mysql(df):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')  # make sure this matches your .env key
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Create table if it doesn't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data (
                Date DATE,
                Invoice_No VARCHAR(20),
                Customer_Name VARCHAR(255),
                Product VARCHAR(255),
                Quantity INT,
                Price DECIMAL(10,2),
                Region VARCHAR(50)
            )
            """)

            # Clear old data before inserting new data
            cursor.execute("DELETE FROM sales_data")
            connection.commit()

            # Insert data into the table
            for _, row in df.iterrows():
                cursor.execute("""
                INSERT INTO sales_data (Date, Invoice_No, Customer_Name, Product, Quantity, Price, Region)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, tuple(row))

            connection.commit()
            print("Data loaded to MySQL successfully!")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    df = read_google_sheet()
    load_data_to_mysql(df)


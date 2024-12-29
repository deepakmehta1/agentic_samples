import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

def load_sql_file(file_path):
    """
    Reads the SQL file and returns the SQL commands as a string.
    :param file_path: Path to the SQL file
    :return: SQL commands as a string
    """
    with open(file_path, 'r') as file:
        return file.read()

def execute_sql(sql_commands):
    """
    Executes SQL commands on the PostgreSQL database.
    :param sql_commands: The SQL commands to execute
    """
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Execute the SQL commands
        cur.execute(sql_commands)
        
        # Commit the transaction
        conn.commit()
        print("SQL commands executed successfully!")

        # Close the cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()

def main():
    # Load the schema and data files
    schema_sql = load_sql_file('db/flight_db_schema.sql')
    data_sql = load_sql_file('db/flight_db_data.sql')

    # Execute schema creation
    print("Creating schema...")
    execute_sql(schema_sql)

    # Execute data insertion
    print("Inserting data...")
    execute_sql(data_sql)

if __name__ == '__main__':
    main()

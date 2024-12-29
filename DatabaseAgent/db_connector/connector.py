# DATABASEAGENT/db_connector/connector.py

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


class DBConnector:
    def __init__(self):
        """Initialize the database connection."""
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish connection to the PostgreSQL database."""
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    host=DB_HOST,
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    port=DB_PORT,
                )
                self.cursor = self.connection.cursor()
                print("Database connection established.")
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                raise

    def execute_query(self, query: str, params: tuple = None):
        """Execute a raw SQL query."""
        if self.connection is None:
            self.connect()

        try:
            # If parameters are passed, execute with parameters
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Commit the transaction if it's a modifying query
            if query.strip().lower().startswith(("insert", "update", "delete")):
                self.connection.commit()

            # Fetch results if it's a SELECT query
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()

        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def close(self):
        """Close the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

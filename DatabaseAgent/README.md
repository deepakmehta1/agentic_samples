# DatabaseAgent - PostgreSQL Database Query Agent

This project provides a **Database Agent** that enables direct querying from a PostgreSQL database. It is capable of executing **multiple and complex queries** to retrieve data and answer the user's query. The agent breaks down complex queries into smaller ones, processes them sequentially, and returns the results in a human-readable format. Whether the query is a `SELECT`, `INSERT`, `UPDATE`, or `DELETE`, the agent ensures accurate and efficient query execution.


## Features

- Connects to a PostgreSQL database.
- Executes raw SQL queries (with support for parameters).
- Returns the result of `SELECT` queries as a string.
- Handles `INSERT`, `UPDATE`, and `DELETE` queries with a success message.


## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
    ```
   
2. Navigate to the project directory:

   ```bash
   cd DatabaseAgent
    ```
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
    ```
4. Make sure you create database flight_db in your postgres database.

5. Make sure you update the .env with correct values.

6. Run the agent:
   ```bash
   python3 main.py
    ```

Give it a star if you got something out of it. :) 
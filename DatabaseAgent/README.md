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

6. Load the DB Schema and data
   ```bash
   python3 db/load_data.py
    ```

7. Run the agent:
   ```bash
   python3 main.py
    ```

## Example execution

```json

[
  {
    "role": "user",
    "content": "Do we have flghts between Los Angeles to Mumbai in Jan 2024?"
  },
  {
    "role": "function",
    "content": "Tool result for {\"query\": \"SELECT city_id FROM city WHERE city_name = 'Los Angeles';\"}: (1,)",
    "name": "sql_query_executer"
  },
  {
    "role": "function",
    "content": "Tool result for {\"query\": \"SELECT city_id FROM city WHERE city_name = 'Mumbai';\"}: (3,)",
    "name": "sql_query_executer"
  },
  {
    "role": "function",
    "content": "Tool result for {\"query\":\"SELECT * FROM flight WHERE source_city_id = 1 AND dest_city_id = 3 AND flight_date BETWEEN '2024-01-01' AND '2024-01-31';\"}: (1, 1, 1, 3, datetime.datetime(2024, 1, 5, 10, 0))",
    "name": "sql_query_executer"
  },
  {
    "role": "assistant",
    "content": "Yes, there is a flight from Los Angeles to Mumbai in January 2024. The flight is scheduled for January 5th, 2024 at 10:00 AM."
  }
]
```

Give it a star if you got something out of it. :) 

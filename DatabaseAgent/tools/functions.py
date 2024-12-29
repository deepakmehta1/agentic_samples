# tools/functions.py
from ..db_connector.connector import DBConnector


def sql_query_executer(db: DBConnector, query: str):
    return db.execute_query(query)

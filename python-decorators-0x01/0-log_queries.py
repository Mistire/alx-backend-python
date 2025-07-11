import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sql_query = args[0] if args else kwargs.get('query')
        print(f"Executing SQL query: {sql_query}")

        try:
            result = func(*args, **kwargs)
            print("SQL query executed successfully.")
            return result
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            raise
        
    return wrapper
        


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
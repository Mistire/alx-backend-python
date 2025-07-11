import sqlite3
import functools
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#### decorator to lof SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sql_query = args[0] if args else kwargs.get('query')
        logger.info(f"Executing SQL query: {sql_query}")

        try:
            result = func(*args, **kwargs)
            logger.info("SQL query executed successfully.")
            return result
        except Exception as e:
            logger.error(f"Error executing SQL query: {e}")
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
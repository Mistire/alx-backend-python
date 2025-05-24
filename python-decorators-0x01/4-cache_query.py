import time
import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("test.db")
        try:
            res = func(conn, *args, **kwargs)
            return res
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query')
        if query in query_cache:
            return query_cache[query]
        else:
            res = func(conn, *args, **kwargs)
            query_cache[query] = res
            return res
    return wrapper

            
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
import time
import sqlite3 
import functools

#### paste your with_db_decorator here

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

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            for attempt in range(1, retries + 1):
              try:
                  res = func(conn, *args, **kwargs)
                  return res
              except Exception as e:
                  print(f"Attempt {attempt}: Error {e}")
                  if attempt == retries:
                      raise
                  time.sleep(delay)
        return wrapper
    return decorator
                    



@with_db_connection
@retry_on_failure(retries=3, delay=1)


def fetch_users_with_retry(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
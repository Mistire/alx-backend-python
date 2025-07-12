import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""
def retry_on_failure(retries, delay):
  def decorator(func):
    def wrapper(*args, **kwargs):
      for attempt in range(retries + 1):
        try:
          return func(*args, **kwargs)
        except Exception as e:
          if attempt < retries:
            time.sleep(delay)
      return func(*args, **kwargs)
    return wrapper
  return decorator

def with_db_connection(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    try:
      conn = sqlite3.connect('user.db')
      print("Successfully created a connection")
      result = func(*args, **kwargs)
      conn.close()
    except sqlite3.Error as e:
      print(f"An error occurred: {e}")
    return result
  return wrapper



@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM users")
  return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
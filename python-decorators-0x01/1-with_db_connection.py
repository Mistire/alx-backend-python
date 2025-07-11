import sqlite3 
import functools
import mysql.connector

def with_db_connection(func):
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
def get_user_by_id(conn, user_id): 
  cursor = conn.cursor() 
  cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
  return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
import sqlite3 
import functools

"""your code goes here"""

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
    
def transactional(func):
  def wrapper(*args, **kwargs):
    conn = args[0] if args else kwargs.get('kwargs')
    try:
      result = func(*args, **kwargs)
      if result.error():
        conn.rollback()
      else:
        conn.commit()
    except sqlite3.Error as e:
      print(f"An error occurred: {e}")
    return result
  return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
  cursor = conn.cursor() 
  cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
import sqlite3

class ExecuteQuery:
  def __init__(self, db_name, query, params=None):
    self.db_name = db_name
    self.query = query
    self.params = params
    self.connection = None

  def __enter__(self):
    self.connection = sqlite3.connect(self.db_name)
    cursor = self.connection.cursor()
    cursor.execute(self.query, self.params)
    return cursor
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.connection:
      if exc_type:
        self.connection.rollback()
      else:
        self.connection.commit()
      self.connection.close()
    return False
  
with ExecuteQuery("test.db", "SELECT * FROM users WHERE age > ?", (25, )) as exec_query:
  result = exec_query.fetchall()
  print(result)

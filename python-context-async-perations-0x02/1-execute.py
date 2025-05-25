import sqlite3

class ExecuteQuery:
  def __init__(self, db_name, db_query, db_query_param=None):
    self.db_name = db_name
    self.db_query = db_query
    self.db_query_param = db_query_param

  def __enter__(self):
    self.conn = sqlite3.connect("test.db")
    self.cursor = self.conn.cursor()
    
    if self.db_query_param is not None:
      self.cursor.execute(self.db_query, self.db_query_param)
    else:
      self.cursor.execute(self.db_query)
    self.cursor.fetchall()

  def __exit__(self, exc_type, exc_val, exc_tb):
    if exc_type:
      self.conn.rollback()
    else:
      self.conn.commit()
    self.conn.close()
    self.cursor.close()

with ExecuteQuery("test.db", "ELECT * FROM users WHERE age > ?", (25,)) as result:
  print(result)

      

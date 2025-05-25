import sqlite3

class DatabaseConnection:
  def __init__(self, db_name):
    self.db_name = db_name
    self.conn = None

  def __enter__(self):
    print("Entering the DB...")
    self.conn = sqlite3.connect(self.db_name)
    return self.conn
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    print("Closing DB...")
    if self.conn:
      self.conn.close()

with DatabaseConnection("test.db") as dbc:
  cursor = dbc.cursor()
  cursor.execute("SELECT * FROM users")
  result = cursor.fetchall()
  print(result)
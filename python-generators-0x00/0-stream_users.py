import mysql.connector

def stream_users():
  connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='remi3721',
    database='ALX_PRO_DEV'
  )

  cursor = connection.cursor(dictionary=True)
  cursor.execute("SELECT * FROM user_data;")

  while True:
    row = cursor.fetchone()
    if row is None:
      break
    yield row

  cursor.close()
  connection.close()
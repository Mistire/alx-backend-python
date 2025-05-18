import mysql.connector

def stream_users_in_batches(batch_size):
  connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="remi3721",
    database="ALX_prodev"
  )

  cursor = connection.cursor(dictionary=True)
  cursor.execute("SELECT * FROM user_data")

  while True:
    rows = cursor.fetchmany(batch_size)
    if not rows:
      break
    yield rows

  cursor.close()
  connection.close()

def batch_processing(batch_size):
  for batch in stream_users_in_batches(batch_size):
    for user in batch:
      if int(user['age']) > 25:
        yield user
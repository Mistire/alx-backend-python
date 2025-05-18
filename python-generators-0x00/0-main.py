#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
  seed.create_database(connection)
  connection.close()
  print("Connection successful")

  connection = seed.connect_to_prodev()
  if connection:
    seed.create_table(connection)
    seed.insert_data(connection, 'user_data.csv')

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT 5;")
    print("Sample data from DB:")
    for row in cursor.fetchall():
      print(row)
    cursor.close()
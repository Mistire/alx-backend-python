import mysql.connector
import csv
import uuid

def connect_db():
  try:
    connection = mysql.connector.connect(
      host="localhost",
      user="root",
      password="remi3721"
    )
    return connection
  except mysql.connector.Error as err:
    print(f"Connection error: {err}")
    return None
  
def create_database(connection):
  cursor = connection.cursor()
  cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
  print("Databse ALX_prodev created")
  cursor.close()

def connect_to_prodev():
  try:
    connection = mysql.connector.connect(
      host="localhost",
      user="root",
      password="remi3721",
      database="ALX_prodev"
    )
    return connection
  except mysql.connector.Error as err:
    print(f"Connection error: {err}")
    return None
  
def create_table(connection):
  cursor = connection.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
      user_id VARCHAR(50) PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      email VARCHAR(255) NOT NULL,
      age DECIMAL NOT NULL
    )
""")
  print("Table User_data created")
  cursor.close()

def insert_data(connection, csv_file):
  cursor = connection.cursor()
  with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
      generated_uuid = str(uuid.uuid4())
      name = row['name']
      email = row['email']
      age = row['age']
      cursor.execute("""
        INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)
""", (generated_uuid, name, email, age))
  connection.commit()
  print("Database inserted from CSV")
  cursor.close()

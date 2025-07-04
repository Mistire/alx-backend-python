import mysql.connector

def connect_db():
  connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "remi3721"
  )

def create_databse(connection):
  cursor = connection.cursor()
  cursor.execute("CREATE DATABASE ALX_PRODEV IF NOT EXISTS")

def connect_to_prodev():
  connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "remi3721",
    database = "ALX_PRODEV"
  )

def create_table(connection):
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS user_data (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, age DECIMAL NOT NULL)")
  cursor.close()
  connection.commit()

def insert_data(connection, data):
  cursor = connection.cursor()
  cursor.execute("INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)", data)
  cursor.close()
  connection.commit()
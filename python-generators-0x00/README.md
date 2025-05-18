
# Python Generators - Task 0: Streaming Rows from MySQL

This task sets up a MySQL database and populates it with user data from a CSV file using Python.

## What the script does

- Connects to MySQL server
- Creates a database `ALX_prodev` if it doesn't exist
- Creates a table `user_data` with fields: `user_id`, `name`, `email`, `age`
- Loads data from `user_data.csv` into the table
- Prints 5 sample rows from the table

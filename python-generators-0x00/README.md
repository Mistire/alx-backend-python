### `python-generators-0x00` - ALX Backend Python

This project demonstrates how to use Python generators to efficiently interact with a MySQL database.


#### Task 0: Getting Started with Python Generators

* Set up MySQL database `ALX_prodev` and a `user_data` table.
* Loaded sample data from a CSV file (`user_data.csv`).
* Functions implemented:

  * `connect_db()`
  * `create_database(connection)`
  * `connect_to_prodev()`
  * `create_table(connection)`
  * `insert_data(connection, data)`


#### Task 1: Generator That Streams Rows

* Implemented a generator function `stream_users()` in `0-stream_users.py`.
* Streams rows from the `user_data` table **one at a time** using Python's `yield`.
* Efficient for working with large datasets.


#### Task 2: Batch Processing Large Data

- Implemented a generator that streams users in batches from the SQL database.
- Filtered users over age 25 during processing.
- Functions:
  - `stream_users_in_batches(batch_size)`
  - `batch_processing(batch_size)`

#### 3. Task3: Lazy Loading Paginated Data
  
- Created `paginate_users(page_size, offset)` to fetch a page of rows with SQL LIMIT and OFFSET.  
- Created `lazy_paginate(page_size)` generator that yields pages of users on demand.  
- Uses a single loop and stops when no more data is returned.  
- Efficiently loads large datasets page-by-page without loading all rows at once.

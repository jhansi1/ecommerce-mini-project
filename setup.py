#one time setup
import sqlite3

# Queries to create tables
customer_sql_query = "CREATE TABLE Customers ( customer_id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, level INT NOT NULL, CHECK(level in (0, 1, 2)));"

vendor_sql_query = "CREATE TABLE Vendors ( vendor_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INT NOT NULL, store_name TEXT NOT NULL, FOREIGN KEY(customer_id) REFERENCES Customers(customer_id));"

item_sql_query = "CREATE TABLE Items (item_id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT NOT NULL, vendor_id INT NOT NULL, available_quantity INT NOT NULL, unit_price REAL NOT NULL, CHECK(available_quantity >= 0 AND unit_price >= 0), FOREIGN KEY(vendor_id) REFERENCES Vendors(vendor_id));"

order_sql_query = "CREATE TABLE Orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INT NOT NULL, item_id INT NOT NULL, quantity INT NOT NULL, FOREIGN KEY(customer_id) REFERENCES Customers(customer_id), FOREIGN KEY(item_id) REFERENCES Items(item_id));"

conn = sqlite3.connect("ecommerce.db") #create or open the DB
conn.execute('PRAGMA foreign_keys = ON') #enable foreign key constraint

cur = conn.cursor()
cur.execute(customer_sql_query)
cur.execute(vendor_sql_query)
cur.execute(item_sql_query)
cur.execute(order_sql_query)

conn.commit() #journaling
conn.close() #write to file
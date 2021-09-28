# A class representing models.
import sqlite3 as sql


def insert_customer(fullname, username, password, level):
    """ Adds new customers to the database. """
    try:
        # Connect to DB
        with sql.connect("ecommerce.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Customers(full_name, username, password, level) VALUES(?,?,?,?)",
                        (fullname, username, password, level))
            con.commit()
            status = 200
            msg = "Customer successfully added"
    except Exception as e:
        con.rollback()
        status = 400
        msg = e
    finally:
        con.close()
        return {"status": status, "message": str(msg)}


def get_all_customers():
    """ Returns all customer details from the database. """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM CUSTOMERS")
    items = res.fetchall()
    item_dict = {}
    for item in items:
        item_dict[item[2]] = {'customer_id': item[0], 'full_name': item[1],
                              'username': item[2], 'password': item[3], 'level': item[4]}
    con.close()
    return {"customers": item_dict}


def search_customer_by_name(username):
    """ Fetches and returns all customers that match with the given name  """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM CUSTOMERS WHERE username = '%s'" % (username))
    ret_val = res.fetchone()
    con.close()
    return ret_val


def insert_vendor(customerid, storename):
    """ Adds new vendors to the database. """
    try:
        with sql.connect("ecommerce.db") as con:
            con.execute("PRAGMA foreign_keys = ON;")
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Vendors(customer_id, store_name) VALUES(?,?)", (customerid, storename))
            con.commit()
            status = 200
            msg = "Vendor successfully added"
    except Exception as e:
        con.rollback()
        status = 400
        msg = e
    finally:
        con.close()
        return {"status": status, "message": str(msg)}


def get_all_vendors():
    """ Returns all vendors details from the database. """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM VENDORS")
    items = res.fetchall()
    item_dict = {}
    for item in items:
        item_dict[item[0]] = {'vendor_id': item[0],
                              'customer_id': item[1], 'store_name': item[2]}
    con.close()
    return {"vendors": item_dict}

def is_vendor(customer_id):
    """ Returns True if the given customer_id is a vendor(level=1), otherwise False  """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM CUSTOMERS WHERE customer_id = %d AND level = 1"% (customer_id))
    item = res.fetchone()
    con.close()
    return True if item else False

def insert_item(item_name, vendor_id, available_quantity, unit_price):
    """ Adds new items to the database. """
    try:
        with sql.connect("ecommerce.db") as con:
            con.execute("PRAGMA foreign_keys = ON;")
            cur = con.cursor()
            cur.execute("INSERT INTO Items(item_name, vendor_id, available_quantity, unit_price) VALUES(?,?,?,?)",
                        (item_name, vendor_id, available_quantity, unit_price))
            con.commit()
            status = 200
            msg = "Item successfully added"
    except Exception as e:
        con.rollback()
        status = 400
        msg = e
    finally:
        con.close()
        return {"status": status, "message": str(msg)}


def get_all_items():
    """ Returns all item details from the database. """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM ITEMS")
    items = res.fetchall()
    item_dict = {}
    for item in items:
        item_dict[item[0]] = {'item_id': item[0], 'item_name': item[1],
                              'vendor_id': item[2], 'available_quantity': item[3], 'unit_price': item[4]}
    con.close()
    return {"items": item_dict}


def search_item_by_name(itemname):
    """ Returns all items that match with given item name. """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM ITEMS WHERE upper(item_name) = '%s'" % (itemname))
    items = res.fetchall()
    item_dict = {}
    for item in items:
        item_dict[item[0]] = {'item_id': item[0], 'item_name': item[1],
                              'vendor_id': item[2], 'available_quantity': item[3], 'unit_price': item[4]}
    con.close()
    return {"items": item_dict}


def insert_order(customer_id, item_id, quantity):
    """ Adds new order details to the database. """
    try:
        with sql.connect("ecommerce.db") as con:
            con.execute("PRAGMA foreign_keys = ON;")
            cur = con.cursor()
            cur.execute("INSERT INTO Orders(customer_id, item_id, quantity) VALUES(?,?,?)",
                        (customer_id, item_id, quantity))
            con.commit()
            status = 200
            msg = "Order successfully added"
    except Exception as e:
        con.rollback()
        status = 400
        msg = e
    finally:
        con.close()
        return {"status": status, "message": str(msg)}


def get_all_orders_by_customer(customer_id):
    """ Returns all orders that match with the given customer ID. """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM ORDERS WHERE customer_id = %d" % (customer_id))
    items = res.fetchall()
    item_dict = {}
    for item in items:
        item_dict[item[0]] = {
            'order_id': item[0], 'customer_id': item[1], 'item_id': item[2], 'quantity': item[3]}
    con.close()
    return {"Orders": item_dict}


def get_all_orders():
    """ Returns all order details from the database. """
    con = sql.connect("ecommerce.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM ORDERS")
    items = res.fetchall()
    item_dict = {}
    for item in items:
        item_dict[item[0]] = {
            'order_id': item[0], 'customer_id': item[1], 'item_id': item[2], 'quantity': item[3]}
    con.close()
    return {"Orders": item_dict}

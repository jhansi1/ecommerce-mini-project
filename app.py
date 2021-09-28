from flask import Flask, jsonify, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt
import models

app = Flask(__name__)
app.secret_key = 'super secret string'
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, level):
        self.id = id
        self.level = level
        self.authenticated = False

    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.id


@login_manager.user_loader
def load_user(username):
    response = models.search_customer_by_name(username)
    if response is None:
        return None
    else:
        return User(response[2], response[4])


@login_required
def get_all_customers():
    response = models.get_all_customers()
    return response


@app.route('/customers', methods=['GET', 'POST'])
def add_customer():
    """GET request: Display all customers in the database.
       POST request: Adds new customers to the database.
    """
    if request.method == 'GET':
        response = get_all_customers()
    elif request.method == 'POST':
        data = request.get_json()
        if current_user.get_id() is None:
            if data:
                if data.get("username", None) and data.get("password", None) and (str(data.get("level", None)) if data.get("level", None) is not None else None):
                    fullname = data["full_name"]
                    username = data["username"]
                    hashed_password = bcrypt.generate_password_hash(
                        data["password"]).decode('utf-8')
                    level = data["level"]
                    response = models.insert_customer(
                        fullname, username, hashed_password, level)
                else:
                    response = {
                        "message": "Username, Password and Level data is mandatory to signup/register", "status": 400}
            else:
                response = {
                    "message": "Please provide required data to signup/register", "status": 400}
        else:
            response = unauthorized_handler()
    return jsonify(response)


@login_required
def get_all_vendors():
    response = models.get_all_vendors()
    return response


@app.route('/vendors', methods=['GET', 'POST'])
def add_vendor():
    """GET request: Display all vendors in the database.
       POST request: Adds new vendors to the database.
    """
    if request.method == 'GET':
        response = get_all_vendors()
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            if data.get("customer_id", None) and data.get("store_name", None) and models.is_vendor(data["customer_id"]):
                customerid = data["customer_id"]
                storename = data["store_name"]
                response = models.insert_vendor(
                    customerid, storename)
            else:
                response = {
                    "message": "Your registered Customer ID and Store name fields are mandatory to add a vendor", "status": 400}
        else:
            response = {
                "message": "Your registered Customer ID and Store name fields are mandatory to add a vendor", "status": 400}
    return jsonify(response)


@app.route('/items', methods=['GET', 'POST'])
@login_required
def add_item():
    """GET request: Display all items in the database.
       POST request: Adds new items to the database.
    """
    if request.method == 'GET':
        response = models.get_all_items()
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            if data.get("item_name", None) and data.get("vendor_id", None) and data.get("available_quantity", None) and data.get("unit_price", None):
                item_name = data["item_name"]
                vendor_id = data["vendor_id"]
                available_quantity = data["available_quantity"]
                unit_price = data["unit_price"]

                # Only logged in vendors can add items. NOTE: level of vendor is 1
                if current_user.level == 1:
                    response = models.insert_item(
                        item_name, vendor_id, available_quantity, unit_price)
                else:
                    response = {
                        "message": "Only logged in vendors can add items", "status": 400}
            else:
                response = {
                    "message": "Itemname, Vendor ID, Available Quantity and Unit price must be entered to add an item", "status": 400}
        else:
            response = {
                "message": "Please enter the required data to add an item", "status": 400}
    return jsonify(response)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def place_order():
    """GET request: Display all orders in the database.
       POST request: Adds new orders to the database.
    """
    if request.method == 'GET':
        # Only the admin can call this API. NOTE: Level of Admin is 2
        if current_user.level == 2:
            response = models.get_all_orders()
        else:
            response = {
                "message": 'You are unauthorized to make this request.', "status": 401}
    elif request.method == 'POST':
        data = request.get_json()
        if data:
            if data.get("customer_id", None) and data.get("item_id", None) and data.get("quantity", None):
                customer_id = data["customer_id"]
                item_id = data["item_id"]
                quantity = data["quantity"]

                # Only logged in customers can place orders. NOTE: level of customer is 0
                if current_user.level == 0:
                    response = models.insert_order(
                        customer_id, item_id, quantity)
                else:
                    response = {
                        "message": "Only logged in customers can place orders", "status": 400}
            else:
                response = {
                    "message": "Customer ID, Item ID and Quantity must be entered to place orders", "status": 400}
        else:
            response = {
                "message": "Please enter the required data to place orders", "status": 400}
    return jsonify(response)


@app.route('/items/<item_name>', methods=['GET'])
@login_required
def search_item_by_name(item_name):
    # Any logged-in customer or vendor can call this API.
    if current_user.level == 1 or current_user.level == 0:
        response = models.search_item_by_name(str(item_name).upper())
    else:
        response = {
            "message": 'You are unauthorized to make this request.', "status": 401}
    return jsonify(response)


@app.route('/orders/<customer_id>', methods=['GET'])
@login_required
def get_all_orders_by_customer(customer_id):
    response = models.get_all_orders_by_customer(
        int(customer_id))
    return jsonify(response)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    if current_user.is_authenticated:
        return redirect(url_for('protected'))

    if request.method == 'POST':
        data = request.get_json()
        if data:
            if data.get("username", None) and data.get("password", None):
                username = data['username']
                user_db_res = models.search_customer_by_name(username)
                password = user_db_res[3]

                # check if the user actually exists
                # take the user-supplied password, hash it, and compare it to the hashed password in the database
                if user_db_res and bcrypt.check_password_hash(password, data['password']):

                    # Login and validate the user. user should be an instance of the `User` class
                    user = load_user(username)
                    login_user(user)
                    return redirect(url_for('protected'))
            else:
                return jsonify({"message": "You must provide username and password to login!", "status": 400})
    return jsonify({"message": "Bad login!", "status": 400})


@app.route('/protected')
@login_required
def protected():
    return jsonify({"message": 'Logged in as: ' + current_user.id, "status": 200})


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout/authentication/session management."""
    logout_user()
    return 'You are logged out!'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return {"message": 'You are unauthorized to make this request.', "status": 401}


if __name__ == '__main__':
    app.run(debug=True)

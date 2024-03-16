"""
Student name(s): Roy Jiang, Aaron Zhao
Student email(s): rjiang@caltech.edu, azhao2@caltech.edu
Supply chain program for a fast food chain 
******************************************************************************
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True


# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='restsupplyadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='password',
          database='final' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (a) - See customer orders')
    print('  (b) - Check supply inventory')
    print('  (c) - Check profit records')
    print('  (d) - Check supplier directory')
    print('  (e) - Place supply order')
    print('  (f) - Update inventory')
    print('  (g) - Add new user')
    print('  (h) - Change user password')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        view_orders()
    elif ans == 'b':
        check_inventory()
    elif ans == 'c':
        check_profits()
    elif ans == 'd':
        check_suppliers()
    elif ans == 'e':
        place_supply_order()
    elif ans == 'f':
        update_inventory()
    elif ans == 'g':
        new_username = input("Enter new username: ")
        password = input("Enter new user password: ")
        is_admin = input("Is admin (0 for no, 1 for yes): ")
        add_new_user(new_username, password, int(is_admin))
    elif ans == 'h':
        username = input("Enter username: ")
        new_password = input("Enter new password: ")
        change_user_password(username, new_password)
    else:
        print('That\'s not one of the options. Please try again.\n')
        show_options()


def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def view_orders():
    """
    Allows the user to see all orders made
    """
    cursor = conn.cursor()
    sql = '''SELECT co_id, qty, name FROM cust_order NATURAL JOIN 
    menu_item GROUP BY co_id;''' 
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('No active orders! Go scrub the tables.')
        else:
            for row in rows:
                (co_id, qty, name) = (row) # tuple unpacking!
                print(f'customer #{co_id}: {qty} x {name}')
        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('your database broke.')


def check_inventory():
    """
    Pulls up the current state of the inventory
    """
    cursor = conn.cursor()
    sql = 'SELECT name, qty_in_stock, unit FROM ingredient;' 
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('We should really order more ingredients...')
        else:
            for row in rows:
                (name, qty, unit) = (row) # tuple unpacking!
                print(f'{name}: {qty} {unit}')
        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('your database broke.')


def check_profits():
    """
    Checks the total profit made across all orders
    """
    cursor = conn.cursor()
    sql = 'select sum(calculate_total_order_cost(co_id)) from cust_order;' 
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('We had no customers... like at all')
        else:
            for row in rows:
                (profit) = (row) # tuple unpacking!
                print(f'We have made ${round(float(profit[0]),2)} USD.')
        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('your database broke.')


def check_suppliers():
    """
    Displays all the suppliers with their contact info
    """
    cursor = conn.cursor()
    sql = 'SELECT name, email, phone FROM supplier;' 
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('No suppliers found')
        else:
            for row in rows:
                (name, email, phone) = (row) # tuple unpacking!
                print(f'{name} \t||\t {email} \t||\t {phone}')
        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('your database broke.')


def place_supply_order():
    """
    Takes input from user specifying which ingredient to order, along with 
    quantity, price, and supplier to place a supply order
    """
    cursor = conn.cursor()
    sql = 'SELECT ingredient_id, name, qty_in_stock, unit FROM ingredient;' 
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        
        if len(rows) == 0:
            print('We have no ingredients. We cannot orders ingredients we never had.')
        else: 
            valid_ing_ids = []
            for row in rows:
                (ingredient_id, name, qty_in_stock, unit) = (row) # tuple unpacking!
                valid_ing_ids.append(ingredient_id)
                print(f'{ingredient_id} \t || \t {name}: {qty_in_stock} {unit}')
            update_ing_id = input('Which ingredient ID are we updating? ')
            while not update_ing_id or int(update_ing_id) not in valid_ing_ids:
                update_ing_id = input('Nonexistent ingredient ID. Enter an existing ID: ')

            sql = 'SELECT supplier_id, name, email, phone FROM supplier;'
            cursor.execute(sql)
            # row = cursor.fetchone()
            rows = cursor.fetchall()

            # due to time, we are just assuming there have to be suppliers. 
            valid_supp_ids = []
            for row in rows:
                (supplier_id, name, email, phone) = (row) # tuple unpacking!
                valid_supp_ids.append(supplier_id)
                print(f'{supplier_id} \t || \t {name} \t||\t {email} \t||\t {phone}')

            update_supp_id = input('Which supplier id? ')
            while not update_supp_id or int(update_supp_id) not in valid_supp_ids:
                update_supp_id = input('Invalid supplier ID. Enter an existing supplier ID: ')

            update_qty = input('How many are we ordering? ')
            while not update_qty or int(update_qty) <= 0:
                update_qty = input('We definitely ordered a positive number: ')

            update_ppu = input('How much does it cost per unit? ')
            while not update_ppu or int(update_ppu) <= 0:
                update_ppu = input('It definitely costed a positive amount: ')

            sql = '''CALL insert_new_supply_order(\'%d\', 
            \'%d\', \'%d\', 
            \'%d\')''' % (int(update_ing_id), int(update_qty), 
                int(update_supp_id), int(update_ppu))
            cursor.execute(sql)
            print('Order inserted!')
        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('your database broke.')


def update_inventory():
    """
    Updates the inventory manually based on user input. 
    """
    cursor = conn.cursor()
    sql = 'SELECT ingredient_id, name, qty_in_stock, unit FROM ingredient;' 
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        
        if len(rows) == 0:
            print('We have no inventory. You can only update inventory when we have inventory.')
        else: 
            valid_ing_ids = []
            for row in rows:
                (ingredient_id, name, qty_in_stock, unit) = (row) # tuple unpacking!
                valid_ing_ids.append(ingredient_id)
                print(f'{ingredient_id} \t || \t {name}: {qty_in_stock} {unit}')
            update_ing_id = input('Which ingredient ID are we updating? ')
            while not update_ing_id or int(update_ing_id) not in valid_ing_ids:
                update_ing_id = input('Nonexistent ingredient ID. Enter an existing ID: ')
            inc_qty_stock = input('How many did we get in the shipment? ')
            while not inc_qty_stock or int(inc_qty_stock) < 0:
                inc_qty_stock = input('''Negative shipment amount. 
                    Shipment amounts must be 0 or positive. Enter valid amount: ''')
            sql = '''CALL update_ingredient_inventory(
                \'%d\', \'%d\')''' % (int(update_ing_id), int(inc_qty_stock))
            cursor.execute(sql)
            print('Updated!')
        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('your database broke.')

def add_new_user(new_username, password, is_admin):
    try:
        with conn.cursor() as cursor:
            # First, check if the username already exists
            cursor.execute("SELECT COUNT(*) FROM user_info WHERE username = %s", (new_username,))
            if cursor.fetchone()[0] > 0:
                print("Username already exists. Please choose a different username.")
                return

            # If the username doesn't exist, proceed to create the new user
            sql = "CALL sp_add_user(%s, %s, %s)"
            cursor.execute(sql, (new_username, password, is_admin))
            conn.commit()
            print(f'New User created: {new_username}')

        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # Handle database errors more gracefully
        if DEBUG:
            print("Error:", err, file=sys.stderr)
        else:
            print('An error occurred with the database operation.', file=sys.stderr)

def change_user_password(username, new_password):
    try:
        with conn.cursor() as cursor:
            # First, check if the user exists
            cursor.execute("SELECT COUNT(*) FROM user_info WHERE username = %s", (username,))
            if cursor.fetchone()[0] == 0:
                print("Username does not exist. Please enter a valid username.")
                return

            # If the user exists, proceed to change the password
            sql = "CALL sp_change_password(%s, %s)"
            cursor.execute(sql, (username, new_password))
            conn.commit()
            print(f"Password for {username} has been updated successfully.")

        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
        # Handle database errors more gracefully
        if DEBUG:
            print("Error:", err, file=sys.stderr)
        else:
            print('An error occurred with the database operation.', file=sys.stderr)

def login_and_authenticate():
    """
    Prompts the user for a username and password, and authenticates the credentials.
    If authentication fails due to incorrect credentials or lack of admin rights,
    appropriate messages are displayed.
    """
    username = input('Username: ')
    password = input('Password: ')

    cursor = conn.cursor()

    # Use parameterized queries to enhance security.
    sql = 'SELECT authenticate(%s, %s) AS login, is_admin FROM user_info WHERE username=%s;'
    params = (username, password, username)

    try:
        cursor.execute(sql, params)
        row = cursor.fetchone()

        if row is None:
            print("Login failed: Username or password incorrect.")
            return False

        login, is_admin = row

        if not login:
            print("Login failed: Username or password incorrect.")
            return False

        if not is_admin:
            print("Access denied: Insufficient privileges.")
            return False

        print(f"Login successful: Welcome, {username}!")
        return True

    except Error as err:
        print(f"System error: {err}. Please contact the system administrator.")
        return False

def main():
    """
    Main function for starting things up.
    """
    if (login_and_authenticate()):
        while(True):
            show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()

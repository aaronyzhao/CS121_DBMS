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
DEBUG = False


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
          user='restsupplyclient',
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


def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  (a) - Place an order')
    print('  (b) - View menu')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        place_order()
    elif ans == 'b':
        view_menu()
    else:
        print('That\'s not one of the options. Please try again.\n')
        show_options()


def place_order():
    """
    Presents option to filter by price
    """
    print('How would you like to proceed? ')
    print('  (a) - Filter by price')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'a':
        filter_menu()
    else:
        print('That\'s not one of the options. Please try again.\n')
        place_order()


def filter_menu():
    """ 
    Allows price filter and then ordering
    """
    cursor = conn.cursor()
    sql = '''SELECT mi.name, mi.description, mi.price_usd
            FROM menu_item mi
            WHERE NOT EXISTS (
                SELECT 1
                FROM mi_contains mc
                JOIN ingredient i ON mc.ingredient_id = i.ingredient_id
                WHERE mc.menu_id = mi.menu_id
                AND mc.qty_req > i.qty_in_stock
            );
            '''
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('Oops, we are all out of stock!')
        else:
            for row in rows:
                (name, desc, price) = (row) # tuple unpacking!
                print(f'{name}: {price}\n{desc}\n')
            threshold = round(int(input('''What is your budget 
                (To the nearest dollar)? Enter 1000 if no budget''')))
            sql1 = f'''SELECT mi.menu_id, mi.name, mi.description, mi.price_usd
                    FROM menu_item mi
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM mi_contains mc
                        JOIN ingredient i ON mc.ingredient_id = i.ingredient_id
                        WHERE mc.menu_id = mi.menu_id
                        AND mc.qty_req > i.qty_in_stock
                    )
                    AND mi.price_usd <= {threshold};
                    '''
            cursor.execute(sql1)
            rows = cursor.fetchall()
            if len(rows) == 0:
                print('It seems you are broke')
            else:
                valid_mids = []
                for row in rows:
                    (id, name, desc, price) = (row) # tuple unpacking!
                    valid_mids.append(int(id))
                    print(f'Menu_id: {id}\n{name}: {price}\n{desc}\n')
        
                m_id = input('Which item ID would you like to order? ')
                while not m_id or int(m_id) not in valid_mids:
                    m_id = input('Sorry, that is not a valid Id. Please select a valid ID: ')

                qty_wanted = input('How many of those would you like? ')
                while not qty_wanted or int(qty_wanted) <= 0:
                    qty_wanted = input('You gotta have at least one... try again: ')
                
                sql = '''CALL insert_new_customer_order(
                    \'%d\', \'%d\')''' % (int(m_id), int(qty_wanted))
                print('Order made!')


        ret = input('Do something else? (y/n) ').lower()
        if ret == 'y':
            show_options()
        else:
            quit_ui()
    except mysql.connector.Error as err:
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


def view_menu():
    """
    Shows the user the entire menu including prices and descriptions
    """
    cursor = conn.cursor()
    cursor = conn.cursor()
    sql = '''SELECT mi.name, mi.description, mi.price_usd
            FROM menu_item mi
            WHERE NOT EXISTS (
                SELECT 1
                FROM mi_contains mc
                JOIN ingredient i ON mc.ingredient_id = i.ingredient_id
                WHERE mc.menu_id = mi.menu_id
                AND mc.qty_req > i.qty_in_stock
            );
            '''
    try:
        cursor.execute(sql)
        # row = cursor.fetchone()
        rows = cursor.fetchall()
        if len(rows) == 0:
            print('Oops, we are all out of stock!')
        else:
            for row in rows:
                (name, desc, price) = (row) # tuple unpacking!
                print(f'{name}: {price}\n{desc}\n')
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

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()

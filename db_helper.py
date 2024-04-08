import mysql.connector
global cnx
cnx = mysql.connector.connect(
    host='localhost',
    user='pandeyji_app',
    password='aryanpatni80137',
    database='pandeyji_eatery'
)

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        #Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        #Commiting the changes
        cnx.commit()

        #Closing the cursor
        cursor.close()

        print("Order item inserted successfully!")
        return 1
    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        #Rollback changes if necessary

        cnx.rollback()

        return -1
    except Exception as e:
        print(f"An  error occurred: {e}")
        # Rollback changes if necessary

        cnx.rollback()
        return -1

def get_order_status(order_id : int):
    #create a cursor object
    cursor = cnx.cursor()
    #write the sql query
    query = ('SELECT status FROM order_tracking WHERE order_id = %s')
    #execute the query
    cursor.execute(query, (order_id,))
    #Fetch the result
    result = cursor.fetchone()
    #close the cursor and connection
    cursor.close()
    if result is not None:
        return result[0]
    else:
        return None

def get_next_order_id():
    cursor = cnx.cursor()
    #Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    #Fetching the result
    result = cursor.fetchone()[0]

    #closing the cursor
    cursor.close()

    #Returning the next available Order_id
    if result is None:
        return 1
    else:
        return result+1

def get_total_order_price(order_id):
    cursor = cnx.cursor()
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))
    cnx.commit()
    cursor.close()

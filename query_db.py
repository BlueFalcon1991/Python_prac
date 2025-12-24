import mysql.connector
from mysql.connector import Error
my_list=[]

def query_database():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="asd123456",
            database="classicmodels"
        )

        if connection.is_connected():
            print("Successfully connected to the database")
            
            # Create a cursor object
            cursor = connection.cursor()
            
            # Define the SQL query to fetch data from a table
            query = "SELECT * FROM classicmodels.products"
            
            # Execute the query
            cursor.execute(query)
            
            # Fetch all results
            results = cursor.fetchall()
            
            # Process the results
            for row in results:
                print(row)
                my_list.append(row)

            # Close the cursor
            cursor.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

# Call the function to query the database
query_database()







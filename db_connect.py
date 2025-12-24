import mysql.connector

# Establish the connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="asd123456",
    database="wf"
)

# Create a cursor object
cursor = connection.cursor()

# Execute a query
cursor.execute("SELECT DATABASE();")

# Fetch the result
result = cursor.fetchone()
print("Connected to database:", result)

# Close the cursor and connection
cursor.close()
connection.close()

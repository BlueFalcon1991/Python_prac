import mysql.connector
import pandas as pd

# 1. Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
            user="root",
            password="asd123456",
            database="classicmodels"
)

# 2. Query the table into a DataFrame
query = "SELECT * FROM classicmodels.orderdetails"
df = pd.read_sql(query, conn)

# 3. Save to Excel
df.to_excel("orderdetails.xlsx", index=False)

# 4. Close the connection
conn.close()

print("Data exported to orderdetails.xlsx")
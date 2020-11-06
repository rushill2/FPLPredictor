# import pyodbc
# server = pyodbc.connect(hostname='myserver.com.au', password='mypassword') # insert our servername here
# row = cursor.fetchone() 
# while row  
#     if (row.status=='injured' || row.status == 'Not Avail')
#         print row
#         row = cursor.fetchone()
import mariadb
conn = mariadb.connect(
        user="fplrecommender_shrikar2",
        password="",
        host="localhost",
        port=3306,
        database="fplrecommender_MainDataDB"
)
print('success')
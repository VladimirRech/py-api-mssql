# POC connecting
import pymssql

conn = pymssql.connect(server='localhost', user='user', password='password', database='manjaro')

# Run query
cursor = conn.cursor()  
cursor.execute('SELECT t.ID, t.TITLE, t.CREATION_DATE, t.UPDATE_DATE FROM tasks t where t.REMOVED = 0 order by t.ID desc;')  
row = cursor.fetchone()  

# loop
while row:  
    print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]))
    row = cursor.fetchone()  

print("Done")
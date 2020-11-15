import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")
conn.execute('DELETE FROM complaints WHERE pincode = 345567 ')

conn.execute('CREATE TABLE complaints (address TEXT NOT NULL, landmark TEXT DEFAULT NULL, state TEXT NOT NULL, pincode NUM NOT NULL, complaint_type TEXT)')
print ("Table created successfully")
conn.close()
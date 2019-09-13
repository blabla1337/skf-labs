import sqlite3

conn = sqlite3.connect('database.db')

print('Opened database successfully')

conn.execute('''CREATE TABLE emptbl
         (ID INT PRIMARY KEY     NOT NULL,
          USERNAME       TEXT    NOT NULL,
          PASSWORD TEXT NOT NULL);''')
print('Table created successfully')
conn.execute("INSERT INTO emptbl (ID,USERNAME,PASSWORD) \
      VALUES (1, 'admin','admin')");
conn.commit()
print('Records created successfully')

command = 'SELECT USERNAME,PASSWORD from emptbl'
result = conn.execute(command)
for row in result:
    username = row
    print(username)
conn.close()

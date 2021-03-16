# Alan Cyriac

import sqlite3
import hashlib

conn = sqlite3.connect('pychat.db')
print ("[+] Opened database successfully")


def createTable(sql, *arg):
    try:
        conn.execute(sql)
        result = True
    except Exception as e:
        print(e)
        result = False
    return str(result)


new_table = '''CREATE TABLE IF NOT EXISTS ADMIN                         \
                    (   ID        INTEGER PRIMARY KEY  AUTOINCREMENT,   \
                        USERNAME  TEXT    NOT NULL,                     \
                        KEY       TEXT    NOT NULL                      \
                    );                                                  \
                '''
table_create = createTable(new_table)

print("[+] Is table Created: " + table_create)


# insert into ADMIN table
username = "Alan" # insert your name to ADMIN table
password = "password" # also insert password but only psw's hash value is saved in the ADMIN table
salt = b'\x15%\xfb\xd1\r\x9d\xd3\xa4\xa9\xfb%\xbd\x14vl\xaa\x1f\xc3q\x86\xf9S\xe5\xe8\x7f\xfd\xd1\xcd\xcf\xcb\xfc\xc7'

# Generating hash value
key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

sql = "INSERT INTO admin (USERNAME, KEY) VALUES (?,?)"
conn.execute(sql, (str(username), str(key),))
conn.commit()
print ("Records created successfully\n\n")

cursor = conn.execute("SELECT * FROM ADMIN")

for row in cursor:
    print(row)

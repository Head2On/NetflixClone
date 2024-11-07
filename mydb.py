# Install mysql on your pc
# pip install mysql-connector
# pip install mysql-connector-python

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '8520',
)
#prepare a cursor object
cursorObject = dataBase.cursor()

#create  a dataBase
cursorObject.execute("CREATE DATABASE Netflix")

print("All Done!")
import sqlite3
import sys
import os
import datetime
from datetime import datetime as dt

con = sqlite3.connect("steam.db") #name of the SQLite database
def createDatabaseTable():
     dbCursor = con.cursor()
     dbCursor.execute("CREATE TABLE steam(date, gamecount, appids)")
     print ("database created... table created")
     insertDummyData()
     print ("yesterday's entry created")

def insertDummyData():
   #until I fix the logic, the main program doesn't like there being no prior items.
    today = dt.now()
    yesterday = today - datetime.timedelta(days= 1)
    yesterday_date = yesterday.strftime("%d-%m-%Y")

    dbCursor = con.cursor()
    dbCursor.execute("INSERT INTO steam('date', 'gamecount', 'appids') VALUES(?,?,?)", (yesterday_date, 0, "0000"))
    con.commit()

    yesterday = today - datetime.timedelta(days= 2)
    yesterday_date = yesterday.strftime("%d-%m-%Y")

    dbCursor = con.cursor()
    dbCursor.execute("INSERT INTO steam('date', 'gamecount', 'appids') VALUES(?,?,?)", (yesterday_date, 0, "0000"))
    con.commit()

def deleteDatabase():
       con.close
       con.close
       os.remove("steam.db")
       print("Database deleted")
       
commandList =['0. Delete database', '1. Create database & table', '2. Drop steam table']
print("Choose option:")

for x in range(len(commandList)):
    print (commandList[x]),

num = int(sys.stdin.readline())
if num == 0:
        deleteDatabase()
elif num == 1:
        createDatabaseTable()
elif num == 2:
      print ("To be implemented")

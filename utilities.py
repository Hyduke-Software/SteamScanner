import sqlite3
import sys
import os
import datetime
from datetime import datetime as dt
#Utiltiies for the SteamScanner application
#Hyduke-Software 2023-2024
#Version 1.0

con = sqlite3.connect("steam.db") #name of the SQLite database

def printAllData():
    dbCursor = con.cursor()
    dbCursor.execute("SELECT * FROM steam")
    rows = dbCursor.fetchall()
    print(rows)

def createDatabaseTable():
     dbCursor = con.cursor()
     dbCursor.execute("CREATE TABLE steam(date, gamecount, appids)")
     print ("database created... table created")
     print ("yesterday's entry created")

def insertDummyData():
    #Enters the previous 2 dates with dummy data
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

def deleteChosenEntry():
     print("enter date in 31-01-2023 format")
     date = sys.stdin.readline().strip()
     dbCursor = con.cursor()
     exestring = "DELETE FROM steam WHERE date =\'{}\'".format(date)
     print(exestring)
     res = dbCursor.execute(exestring)
     con.commit()

def deleteDatabase():
       #Does not quite work yet
       con.close
       con.close
       os.remove("steam.db")
       print("Database deleted")
       
commandList =['0. Delete database', '1. Create database & table', '2. Insert dummy data', '3. Print all rows (abridged)', '4. Delete an entry']
print("Choose option:")

for x in range(len(commandList)):
    print (commandList[x]),

num = int(sys.stdin.readline())
if num == 0:
        deleteDatabase()
elif num == 1:
        createDatabaseTable()
elif num == 2:
        insertDummyData()
elif num ==3:
        printAllData()
elif num ==4:
        deleteChosenEntry()

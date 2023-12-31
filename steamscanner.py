#Hyduke Software 2023
#Version 1.0.1
#This program will check the Steam API for a user's game count, store in an SQLite database, then compare with previous date's count
#Then creates a web page to display, recreated every run of this file
#Default API ignores free games with no playtime

import json
import requests
import sqlite3
import datetime
from datetime import date, timedelta
from datetime import datetime as dt
#todo: fix these datetime imports

#### Initilisations, required values ########
con         = sqlite3.connect("steam.db")
apikey      = ""  #enter your API key from https://steamcommunity.com/dev/apikey
userid      = ""                 #enter the userID from Steam
api_url     = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="+apikey+"&steamid="+userid+"&format=json"
webFileName = "steam.html"


#### Utility sub routines #######
def countCleaner(unclean_Count):
     #cleans a count value returned from SQL as it returns the value like [(420,)]
    cleaned_Count = str(unclean_Count).replace('[','').replace(']','').replace(',','').replace(')','').replace(']','').replace('(','').replace('\'','')
    cleaned_Count.strip()
    return cleaned_Count

def compareDatabaseFormatDateWithToday(lastpurchasedate):
    #Converts the text database date and compares with today
    #todo: spin this off into a function to convert the db string dates into real dates
    lastDay     = int(lastpurchasedate[0]+lastpurchasedate[1])
    lastMonth   = int(lastpurchasedate[3]+lastpurchasedate[4])
    lastYear    = int(lastpurchasedate[6]+lastpurchasedate[7]+lastpurchasedate[8]+lastpurchasedate[9])
    #an unfortunant way to handle time and date- to draws the chars out of the string
    dateOfLastPurchase = datetime.date(day=lastDay, month=lastMonth, year=lastYear, )
    today = dt.now().date()
    delta = today - dateOfLastPurchase
    #calculates the days
    return (delta)

def checkIfTodaysRecordExists():
     #checks the database for today's entry, if so it will not create a new one
    today = dt.now().strftime("%d-%m-%Y")
    sqlString = "SELECT COUNT(*) FROM steam WHERE date ='{}'".format(today) #the current game count value
    print(sqlString)
    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    rows = dbCursor.fetchall()
    result = countCleaner(rows)
    #returns false if row does not exist
    print(result)
    if ( int(result) > 0):
        return True
    elif ( int(result) < 0): 
        return False
    
def rowCounter():
    sqlString = "SELECT COUNT(*) FROM steam"
    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    rows = dbCursor.fetchall()
    result = countCleaner(rows)
    return int(result)

def deleteRow(date):
    #deletes rows matching a date, I expect it would delete all of the same date if they exist
    sqlString = "delete from steam where date='{}'".format(date)
    print(sqlString)
    dbCursor = con.cursor()
    dbCursor.execute(sqlString)

##### Data capture and storage subroutines
def getJSONProcessValues():
    #pulls the game appIDs from the API JSON
    appids      =   []     #array to store the list of game appIDs
    appstring   =   ''     #string to be dumped into the database
    response    =   requests.get(api_url)
    decoded     =   json.loads(response.content.decode())
    games       =   decoded['response']['games']
    
    for game in games:
            appids.append(game['appid'])
    #adds the appIDs to the array
    i = 0
    while i < len(appids):
            appstring += str(appids[i])+','
            i += 1
            #adds the appIDs from the array into a string
    appstring   =   appstring[:-1] #removes a trailing comma in the last value
    return appstring, (len(appids))
#returns the string of appnames and the length of the array. The length is the total game count


def insertIntodatabase():
    #(date, gamecount, appids)
    today = dt.now().strftime("%d-%m-%Y") #gets the date in a 20-10-2023 format
    if (checkIfTodaysRecordExists() == True):
        print("Deleting existing row, recreating")
        deleteRow(today)

    appstring, gameCount = getJSONProcessValues()
    dbCursor = con.cursor()
    dbCursor.execute("INSERT INTO steam('date', 'gamecount', 'appids') VALUES(?,?,?)", (today,gameCount, appstring))
    con.commit()

####################### Comparison subroutines ###########
def findLastPurchase():
    if (countPreviousEntries() < 1):
        return "NEVER"
    today_count_int   =   getTodaysGameCount()
    sqlString = "select date from steam WHERE {0} > gamecount ORDER by date DESC, gamecount LIMIT 1".format(str(today_count_int)) #the current game count value
    print(sqlString)
    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    rows = dbCursor.fetchall()
    print(rows)
    return countCleaner(rows)

def countPreviousEntries():
    #to fix the problem of no previously lower values in findLastPurchase()
    today_count_int   =   getTodaysGameCount()
    sqlString         = "select COUNT(*) from steam WHERE {0} > gamecount".format(str(today_count_int)) #the current game count value
    print(sqlString)
    dbCursor = con.cursor()
    dbCursor.execute(sqlString)
    rows = dbCursor.fetchall()
    print(rows)
    return int(countCleaner(rows))


def getTodaysGameCount():
#compares today's count with yesterday
    today = dt.now().strftime("%d-%m-%Y")
    dbCursor = con.cursor()
    exestring = "SELECT gamecount FROM steam WHERE date =\'"+today+"\'"
    dbCursor.execute(exestring)
    today_count = dbCursor.fetchall()
    clean_today_count = countCleaner(today_count)
    #cast to int and compare
    today_count_int =int(clean_today_count)

    return today_count_int

############ Create web page ###############
def createWebPage():
     today_count_int   =   getTodaysGameCount()
     comment           =   ''
     today = dt.now()
     lastpurchasedate = findLastPurchase()
     if (lastpurchasedate != "NEVER"):
        datediff = compareDatabaseFormatDateWithToday(lastpurchasedate)
        comment ='Days since last game purchase {0}'.format(datediff.days)    #comment on the difference
     elif (lastpurchasedate == "NEVER"):
        comment ='No older data available'  #comment on the difference
     #gets the values
     html ="<html><title>Steam data checker 2000</title><head></head><body style=\"background-color:black;\"><p style=\"color:green\">Page generated at {0}<br>Today's game total:     {1}<br>{2} </body></html>".format(today.strftime("%d-%m-%Y %H:%M"),today_count_int,comment)
     writeWebPageFile (html)

def writeWebPageFile(html):
    with open(webFileName, "w") as webPage:
     webPage.write("{0}".format(html))


############# subroutine calling ###############
insertIntodatabase()
createWebPage()

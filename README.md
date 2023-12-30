# SteamScanner
A tool to track a friend's Steam game purchasing habit

Todo: 30/12/2023
Add the logic so that the program doesn't complain about being no prior rows when first launched.
The two fake entries upon table creation seem to work, but show a 1 days since last purchase.







----------------------------------------------------------------------------------------------------------------
Installation instructions
Python3 required


First run utilities.py 
python3 utilties.py

when prompted enter 1 to create the database and table

then you can run the main program
python3 steamscanner.py
This should then read the API, convert the values and enter into the SQLite database, assuming permissions are correct.
It will then output the HTML file steam.html

I suggest creating a cron job for python3 steamscanner.py
and one to move the steam.html file into your web directory
Example:
This runs the steamscanner file at 22 minutes on every hour then copies the file on the 26th minute, every hour.

22 * * * * cd /opt/steam && python3 steamscanner.py >/dev/null 2>&1
26 * * * * cd /opt/steam  && cp steam.html /var/www/hyduke-software >/dev/null 2>&1


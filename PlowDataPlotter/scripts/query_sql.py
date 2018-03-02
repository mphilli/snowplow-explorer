# a quick script for querying the SQL database
import sqlite3

conn = sqlite3.connect("../resources/plowdata.sqlite")
c = conn.cursor()

query = input("query?> ")
while query != ".quit":
    try:
        c.execute(query)
        result = c.fetchall()
        for r in result:
            print(r)
    except:
        print("Error processing query")
    query = input("query?> ")
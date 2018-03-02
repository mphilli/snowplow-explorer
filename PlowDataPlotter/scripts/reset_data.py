# This script recreates the SQLite sessions database from the provided plowdata.csv file.


import sys
import json_to_sqllite3  # IDE complains because it doesn't know we're just running a script from command line
import csv_to_json
import sessions_table

tg = 15
purge = 50

if 6 > len(sys.argv) > 1:
    if "-tg" in sys.argv:
        if sys.argv.index("-tg")+1 <= len(sys.argv)-1:
            tg_arg = sys.argv[sys.argv.index("-tg") + 1]
            try:
                int(tg_arg)
                tg = tg_arg
            except ValueError:
                pass
    if "-purge" in sys.argv:
        if sys.argv.index("-purge")+1 <= len(sys.argv)-1:
            purge_arg = sys.argv[sys.argv.index("-purge") + 1]
            try:
                int(purge_arg)
                purge = purge_arg
            except ValueError:
                pass

# CSV TO JSON
print("Converting plowdata.csv to plowdata.json")
csv_to_json.main()

# JSON TO SQL
print("Creating plowdata SQLite table from plowdata.json")
json_to_sqllite3.main()

# CREATE SESSIONS TABLE
print("Creating sessions table")
sessions_table.main(time_gap_in=int(tg), purge_val=int(purge))

print("All data has been recreated.")
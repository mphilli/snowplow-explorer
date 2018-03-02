import sqlite3
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt


conn = sqlite3.connect("../resources/plowdata.sqlite")
c = conn.cursor()
COL_NAMES = ["File", "truck_name", "strHeading", "address",
             "activity_type", "latitude", "longitude", "date_ISO"]  # Table column names


def tuple_to_dict(tuple_in):
    """transforms a raw tuple of data for a row into a tagged dictionary"""
    return {"File": tuple_in[1],
            "truck_name": tuple_in[2],
            "strHeading": tuple_in[3],
            "address": tuple_in[4],
            "activity_type": tuple_in[5],
            "latitude": tuple_in[6],
            "longitude": tuple_in[7],
            "date_ISO": tuple_in[8]}


def time_gap(last, this, minutes=15):
    """takes an ISO date and sees if it's more than 20 minutes since the last date"""
    this, last = dt.strptime(this.replace("T", "-").replace(":", "-"), "%Y-%m-%d-%H-%M-%S"), \
                 dt.strptime(last.replace("T", "-").replace(":", "-"), "%Y-%m-%d-%H-%M-%S")
    return last < (this - relativedelta(minutes=minutes))


def create_table():
    """create the sessions table in the SQLite database"""
    try:
        c.execute("""CREATE TABLE sessions 
                    (id INTEGER PRIMARY KEY,
                    File text NOT NULL,
                    truck_name text NOT NULL,
                    strHeading text,
                    address text,
                    activity_type text,
                    latitude text,
                    longitude text,
                    date_ISO text, 
                    session_id INTEGER NOT NULL,
                        foreign key(id) REFERENCES plowdata(id))""")
        conn.commit()
    except sqlite3.OperationalError:
        c.execute("DROP TABLE sessions;")  # recreate the table
        conn.commit()
        create_table()


def get_sessions(tg):
    """transforms the dataset into a sessions-based SQLite table"""
    c.execute("SELECT * FROM plowdata ORDER BY date_ISO")
    result = c.fetchall()
    curr = 0
    data = {}
    for i, r in enumerate(result):
        activity = tuple_to_dict(r)
        if activity['truck_name'] not in data:
            curr += 1
            data[activity['truck_name']] = [(curr, [r + (str(curr),)])]
        else:
            # get latest time from this truck
            # it would be the latest activity in the latest session
            latest_session = data[activity['truck_name']][-1]  # latest session for this truck
            latest_activity = latest_session[1][-1]
            latest_datetime = latest_activity[-2]
            if not time_gap(latest_datetime, activity['date_ISO'], minutes=tg):
                latest_session[1].append(r + (str(latest_session[0]),))
            else:
                curr += 1
                data[activity['truck_name']].append((curr, [r + (str(curr),)]))
        # give a calculations update
        if i % 50000 == 0:
            print(str(i) + " activities calculated...")
    return data


def add_session_sql(sess_data):
    """takes the prepared data and places it into the database"""
    all_entries = []
    for truck in sess_data:
        for tup in sess_data[truck]:
            for act in tup[1]:
                all_entries.append(act)
    c.executemany("insert into sessions(id, File, truck_name, strHeading, address, activity_type, "
                  "latitude, longitude, date_ISO, session_id) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", all_entries)
    conn.commit()


def purge_small_sessions(max_size=50):
    """deletes sessions with less than max_size activities"""
    max_size = str(max_size).replace(";", "")
    print("purging database of sessions with less than " + str(max_size) + " rows...")
    c.execute("SELECT session_id, COUNT(DISTINCT id) FROM sessions GROUP BY session_id HAVING COUNT(DISTINCT id) < " +
              max_size)
    small_sessions = tuple([t[0] for t in c.fetchall()])
    quest = "?, "*len(small_sessions)
    c.execute("DELETE FROM sessions WHERE session_id IN (" + quest[:-2] + ")", small_sessions)
    conn.commit()


def main(time_gap_in=15, purge_val=50):
    """runs all functions in the script to create the sessions table"""
    create_table()
    sessions = get_sessions(time_gap_in)
    add_session_sql(sessions)
    c.execute("DROP TABLE plowdata;")  # no longer needed
    conn.commit()
    purge_small_sessions(max_size=purge_val)

if __name__ == "__main__":
    main()
    purge_small_sessions(max_size=50)
"""
data dictionary structure: 
{"truck_id": 
    [(session 1, 
        [(details), 
         (...)]
    ),
    (2, 
        [...]
    )]
}
"""
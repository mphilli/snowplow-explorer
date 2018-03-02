import sqlite3
import json
from os.path import abspath, dirname, join

conn = sqlite3.connect(join(abspath(dirname(__file__)), "../resources/plowdata.sqlite"))
c = conn.cursor()
COL_NAMES = ["File", "truck_name", "strHeading", "address",
             "activity_type", "latitude", "longitude", "date_ISO"]


def create_table():
    try:
        c.execute("""CREATE TABLE plowdata 
                    (id INTEGER PRIMARY KEY, 
                    File text NOT NULL,
                    truck_name text NOT NULL,
                    strHeading text,
                    address text,
                    activity_type text,
                    latitude text,
                    longitude text,
                    date_ISO text);""")
        conn.commit()
    except sqlite3.OperationalError as op_err:
        c.execute("DROP TABLE plowdata;")  # recreate the table
        conn.commit()
        create_table()
        pass


def insert(**kwargs):
    qs = ("?," * len(kwargs))[:-1]
    vals = [str(arg) for arg in kwargs]
    insert_data = [kwargs[arg] for arg in kwargs]
    sql_in = ("INSERT INTO plowdata (" + str(vals) +
              ") VALUES(" + qs + ")").replace("[", "").replace("]", "")
    c.execute(sql_in, tuple(insert_data))
    conn.commit()


def transform_to_tuples(data_in):
    transformed = [["", ]*8]*len(data_in)
    for i, log in enumerate(data_in):
        for column in log:
            for j, col in enumerate(COL_NAMES):
                if column == col:
                    transformed[i][j] = log[column]
        transformed[i] = tuple(transformed[i])
    return transformed


def transmit_json_data():
    with open(join(abspath(dirname(__file__)), "../resources/plowdata.json"), "r", encoding="UTF-8") as json_file:
        plow_data = transform_to_tuples(json.load(json_file))
        c.executemany("INSERT INTO plowdata(File, truck_name, strHeading, address, activity_type, "
                      "latitude, longitude, date_ISO) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", plow_data)
        conn.commit()


def main():
    create_table()
    transmit_json_data()

if __name__ == "__main__":
    main()

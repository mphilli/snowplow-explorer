import sqlite3
from os.path import join, abspath, dirname
from PlowDataPlotter.TimestampHandler import Timestamp

# hook to SQLite database
DB_PATH = join(abspath(dirname(__file__)), "./resources/plowdata.sqlite")
CONN = sqlite3.connect(DB_PATH)
CRS = CONN.cursor()


class SessionsFromInterval:
    """Create and manage a list of a SessionDataFromInterval objects based on a given interval"""
    def __init__(self, start, end, street=None):
        self.start = start
        self.end = end
        self.sessions_data = self.fetch_sessions()
        self.session_objects = []
        for sess in set([d[-1] for d in self.sessions_data]):
            self.session_objects.append(SessionDataFromInterval(
                [d for d in self.sessions_data if int(d[-1]) == int(sess)],
                self.start, self.end, street=street))
        self.session_objects_street = []
        if street:
            for sess in self.session_objects:
                if sess.street_data and len(sess.street_data) > 0:
                    self.session_objects_street.append(sess)

    def fetch_sessions(self):
        distinct_sess = "SELECT DISTINCT session_id FROM sessions"
        time_query = ' WHERE "' + self.start + '" < date_ISO AND "' + self.end + '" > date_ISO'
        CRS.execute("SElECT * FROM sessions WHERE session_id IN (" + distinct_sess + time_query + ") ORDER BY date_ISO")
        return CRS.fetchall()


class SessionData:
    """A class for handling and labeling the data of a single session (id, truck name, date, etc...)"""
    def __init__(self, session_data=None, session_id=None, street=None):
        if session_id and not session_data:
            session_data = self.get_session(session_id)
        if not session_data:
            self.id = -1
            self.data = []
        else:
            self.id = session_data[0][-1]
            self.data = [self.tuple_to_dict(d) for d in session_data]
            if self.data:
                self.shift_start = Timestamp(self.data[0]["date_ISO"])  # the real start of this shift
                self.shift_end = Timestamp(self.data[-1]["date_ISO"])
                # for map label
                self.truck_id = self.data[0]["truck_name"]
                self.date = self.data[0]["File"]
                self.length = str(round(abs((self.shift_end.datetime
                                             - self.shift_start.datetime).seconds) / 60 / 60, 1))
                if street:
                    self.street = street
                    self.street_data = [d for d in self.data
                                        if self.street.lower()
                                        in d["address"].lower()]

    def get_coordinates(self):
        coordinates = []
        for i, log in enumerate(self.data):
            long, lat = float(log['longitude']), float(log['latitude'])
            coordinates.append([lat, long])
        return coordinates

    def get_session(self, s_id):
        CRS.execute("SElECT * FROM sessions  WHERE session_id=" + str(s_id) + " ORDER BY date_ISO")
        return CRS.fetchall()

    @staticmethod
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


class SessionDataFromInterval(SessionData):
    """A class for handling a session object's data between a certain time period.
       Used when plotting snippets of multiple sessions between the user's specified timeframe."""
    def __init__(self, session_data, start_interval, end_interval, street=None):
        self.start_interval = start_interval  # the start of the interval
        self.end_interval = end_interval
        super().__init__(session_data, street=street)
        self.data = self._create_truncated_data()

    def _create_truncated_data(self):
        return [d for d in self.data
                if self.start_interval <= d["date_ISO"] <= self.end_interval]

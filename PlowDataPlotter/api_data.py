from PlowDataPlotter.SessionsHandler import SessionsFromInterval, SessionData


class GetSessionsInfo:

    def __init__(self,
                 session_objs: SessionsFromInterval=None,
                 session: SessionData=None):
        """Follows the same initialization design as the PlotSessions class,
        but just returns the raw info for the API"""
        self.sessions = None
        self.session_objs = session_objs
        if session_objs:
            self.sessions = session_objs
        elif session:
            self.sessions = [session]
        self.info = self.get_sessions_info()

    def get_sessions_info(self):
        sessions_dict = {}
        if self.sessions:
            for sess in self.sessions:
                label_data = {"truck": sess.truck_id, "date": sess.date, "start": str(sess.shift_start),
                              "end": str(sess.shift_end), "length": str(sess.length)}
                sessions_dict[sess.id] = {"data": label_data, "coordinates": sess.get_coordinates()}
        return sessions_dict


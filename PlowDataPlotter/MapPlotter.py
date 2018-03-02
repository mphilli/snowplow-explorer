import random
import folium
from PlowDataPlotter.SessionsHandler import SessionsFromInterval, SessionData
from PlowDataPlotter.TimestampHandler import Timestamp
from os.path import abspath, dirname, join


SYRACUSE_LOC = [43.0493, -76.1455]  # Constant for Syracuse coordinate location
SYRACUSE_COLOR = "#FFA500"  # Syracuse orange for plotting single sessions
ZOOM_CONST = 13  # Zoom parameter


class PlotSessions:

    def __init__(self,
                 session_objs: SessionsFromInterval=None,
                 session: SessionData=None):
        """A simple class for saving new maps with data from the user's query"""
        self.sessions = None
        self.session_objs = session_objs
        self.map = folium.Map(location=SYRACUSE_LOC, zoom_start=ZOOM_CONST)
        if session_objs:
            self.sessions = session_objs
        elif session:
            self.sessions = [session]

    def plot(self, with_markers=False):
        """take coordinates from the session(s) and plot them to the folium map"""
        if self.sessions:
            for sess in self.sessions:
                session_func = "parent.loadsession(" + str(sess.id) + ", false" + ");"
                # create data label for plot lines
                label = "Truck name: " + sess.truck_id + "<br>" + "Date: " + \
                        sess.date + "<br>" + "Time: " + str(sess.shift_start) + " to " + str(sess.shift_end) + \
                        "<br>Session Length: " + \
                    str(sess.length) + " hours<br>Session ID: " + str(sess.id) + "<br>"
                if self.session_objs:
                        # we have interval data of multiple sessions, let's let the user view a single session
                        label += '<a href="#" onclick="' + session_func + '">view full session</a>'
                        label += ' <a href="#" onclick="' + session_func.replace("false", "true") + \
                                 '">(include markers)</a>'
                if len(self.sessions) == 1:
                    color = SYRACUSE_COLOR
                else:
                    color = self.rand_hex()
                if with_markers:
                    coor = sess.get_coordinates() # get the coordinates for this session to plot
                    self.map = folium.Map(location=coor[int(len(coor)/2)], zoom_start=15)
                    for i, each in enumerate(coor):
                            activity = ""
                            address = ' '.join([a.title() for a in sess.data[i]["address"].split(" ")])
                            # create labels for each marker on the map
                            if sess.data[i]["activity_type"] and not "moving" in sess.data[i]["activity_type"].lower():
                                activity = "<b>Activity: " + sess.data[i]["activity_type"] + "</b><br>"
                            marker_label = "Truck: " + sess.truck_id + "<br>" + \
                                           "Coordinates: " + str(each[0]) + \
                                           ", " + str(each[1]) + "<br>" + \
                                           "Address:" + address + "<br>" + activity + \
                                           "Time: " + Timestamp.get_time(sess.data[i]["date_ISO"]) + \
                                           "<br>Session ID: " + str(sess.id)
                            if not activity == "":
                                folium.Marker(each, popup=marker_label).add_to(self.map)
                folium.PolyLine(
                    sess.get_coordinates(),
                    weight=4.4,
                    opacity=0.6,
                    popup=label,
                    color=color).add_to(self.map)
            self.map.save(outfile=join(abspath(dirname(__file__)),"../templates/map.html"))

    @staticmethod
    def rand_hex():
        """returns a random HEX code for a random color to plot the line with."""
        return "#" + ''.join([random.choice('0123456789ABCDEF')
                              for x in range(6)])

from PlowDataPlotter.SessionsHandler import SessionsFromInterval, SessionDataFromInterval, SessionData
from PlowDataPlotter.TimestampHandler import Timestamp


def generate_table_api(sessions_in, street=None):
    """return the information used to make the tables, but as a dictionary"""
    if type(sessions_in) == SessionData:
        if not street:
            sess_objects = [sessions_in]
        else:
            sess_objects = [sessions_in]
    else:
        if not street:
            sess_objects = sessions_in.session_objects
        else:
            sess_objects = sessions_in.session_objects_street
    data_table = {}
    i = 0
    for sess_obj in sess_objects:
        for data in sess_obj.data:
            if not street or street in data["address"].lower():
                i += 1
                data_table[i] = {"session id": str(sess_obj.id), "truck name": str(sess_obj.truck_id),
                                 "latitude": data["latitude"], "longitude": data["longitude"],
                                 "address": " ".join([t.title() for t in data["address"].split(" ")]),
                                 "activity type": data["activity_type"],
                                 "time": str(Timestamp.get_time_s(data["date_ISO"]))}
    return data_table

def generate_table(sessions_in, street=None):
    """generate an HTML table of the sessions data"""

    if type(sessions_in) == SessionData:
        if not street:
            sess_objects = [sessions_in]
        else:
            sess_objects = [sessions_in]
    else:
        if not street:
            sess_objects = sessions_in.session_objects
        else:
            sess_objects = sessions_in.session_objects_street
    table = """<table id="session-table">
                        <col style="width:7%">
                        <col style="width:8%">
                        <col style="width:10%">
                        <col style="width:10%">
                        <col style="width:27%">
                        <col style="width:13%">
                        <col style="width:11%">
                        <thead>
                        <tr>
                            <th>Session ID</th>
                            <th>Truck Name</th>
                            <th>Lat.</th>
                            <th>Long.</th>
                            <th>Address</th>
                            <th>Activity Type</th>
                            <th>Time</th>
                        </tr>
                        </thead>
                        <tbody>
                """
    for sess_obj in sess_objects:
        for data in sess_obj.data:
            if not street or street in data["address"].lower():
                table += "<tr>"
                table += '<td class="session-id"><a href="#" onclick="loadsession(' + str(sess_obj.id) +\
                         ')">' + str(sess_obj.id) + "</a></td>"
                table += "<td>" + str(sess_obj.truck_id) + "</td>"
                table += "<td>" + data["latitude"] + "</td>"
                table += "<td>" + data["longitude"] + "</td>"
                formatted_address = " ".join([t.title() for t in data["address"].split(" ")])
                table += "<td>" + formatted_address + "</td>"
                table += "<td>" + data["activity_type"] + "</td>"
                formatted_time = Timestamp.get_time_s(data["date_ISO"])
                table += "<td>" + str(formatted_time) + "</td>"
                table += "</tr>"
    table += "</tbody></table>"
    return table

if __name__ == "__main__":
    gt = generate_table_api(SessionsFromInterval("2018-01-01T07:00:00", "2018-01-01T08:00:00"))
    print(gt)
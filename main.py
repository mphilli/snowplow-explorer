from flask import Flask, render_template, url_for, send_file, Markup, jsonify
from PlowDataPlotter.MapPlotter import PlotSessions
from PlowDataPlotter.SessionsHandler import SessionData, SessionsFromInterval
from PlowDataPlotter.api_data import GetSessionsInfo
import os
import data_utils

app = Flask(__name__)


@app.route("/")
@app.route("/session/<int:session_id>")
@app.route("/session/<int:session_id>/<from_str>")
@app.route("/interval/<date>/<start>/<end>/")
@app.route("/interval/<date>/<start>/<end>/<street>")
def index(session_id=None, street=None, date=None, start=None, end=None, from_str=None):
    """main function for rendering the index page according to session and interval data"""
    table = None
    if session_id:
        # for plotting a single session
        sess = SessionData(session_id=session_id)
        if sess.data:
            PlotSessions(session=sess).plot()
            table = Markup(data_utils.generate_table(sess))
    if date and start and end:
        # turn incoming dates and times into properly formatted intervals for the session objects
        date_pieces = date.split("-")
        year_month_day = "-".join([date_pieces[2], date_pieces[0], date_pieces[1]])
        start_time = year_month_day + "T" + start.replace("-", ":")
        end_time = year_month_day + "T" + end.replace("-", ":")
        from_interval = SessionsFromInterval(start=start_time, end=end_time, street=street)
        if from_interval.session_objects:
            if street:
                # only plot sessions that come in contact with this street
                PlotSessions(session_objs=from_interval.session_objects_street).plot()
                # only output rows of data including this street
                table = Markup(data_utils.generate_table(from_interval, street=street))
            else:
                PlotSessions(session_objs=from_interval.session_objects).plot()
                table = Markup(data_utils.generate_table(from_interval))
    return render_template("index.html", data_table=table, from_string=from_str)


@app.route("/session/markers/<int:session_id>")
@app.route("/session/markers/<int:session_id>/<from_str>")
def activity_marks(session_id=None, from_str=None):
    """for rendering maps with markers for single sessions"""
    table = None
    if session_id:
        sess = SessionData(session_id=session_id)
        if sess.data:
            PlotSessions(session=sess).plot(with_markers=True)
            table = Markup(data_utils.generate_table(sess))
            return render_template("index.html", data_table=table, from_string=from_str)
    return render_template("index.html")


@app.route("/templates/map.html")
def show_map():
    """render map from file to iframe"""
    return send_file("./templates/map.html", cache_timeout=0)


@app.route("/templates/default_map.html")
def show_default_map():
    """render default (blank) map from file to iframe"""
    return send_file("./templates/default_map.html", cache_timeout=0)


@app.route("/about")
def about_page():
    """display the about page"""
    return render_template("about.html")


@app.route("/api")
def api_home_page():
    """display the api home page"""
    return render_template("api.html")


@app.errorhandler(404)
def page_not_found(e):
    """Render 404 page in case of Not Found error"""
    return render_template('404.html'), 404

@app.route("/api/session/<int:session_id>")
@app.route("/api/session/<int:session_id>/<from_str>")
@app.route("/api/interval/<date>/<start>/<end>/")
@app.route("/api/interval/<date>/<start>/<end>/<street>")
def api(session_id=None, street=None, date=None, start=None, end=None, from_str=None):
    """render the same information as for a regular search query, but as raw JSON for the API mode."""
    table = None
    json_data = {}
    if session_id:
        sess = SessionData(session_id=session_id)
        if sess.data:
            json_data = GetSessionsInfo(session=sess).info
            table = data_utils.generate_table_api(sess)
    elif date and start and end:
        date_pieces = date.split("-")
        year_month_day = "-".join([date_pieces[2], date_pieces[0], date_pieces[1]])
        start_time = year_month_day + "T" + start.replace("-", ":")
        end_time = year_month_day + "T" + end.replace("-", ":")
        from_interval = SessionsFromInterval(start=start_time, end=end_time, street=street)
        if from_interval.session_objects:
            if street:
                json_data = GetSessionsInfo(session_objs=from_interval.session_objects_street).info
                table = data_utils.generate_table_api(from_interval, street=street)
            else:
                json_data = GetSessionsInfo(session_objs=from_interval.session_objects).info
                table = data_utils.generate_table_api(from_interval)

    return jsonify({"Map data": json_data, "Table data": table})


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# to deal with cached static CSS page:
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


if __name__ == "__main__":
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=False)  # run app

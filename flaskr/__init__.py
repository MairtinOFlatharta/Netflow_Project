from flask import Flask, render_template, make_response, request, redirect
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager
from json import loads, dumps

from .model import User, Nfdump_data


data_instance = None


def create_app():
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__)

    # Config is external JSON file for now. Better than commiting keys
    app.config.from_json('../instance/config.json')

    if app.config['LOCAL_DB']:
        app.config['MONGODB_SETTINGS']['host'] = 'mongodb://127.0.0.1:27017/'

    # Setup Flask-MongoEngine
    db = MongoEngine(app)

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        # String-based templates
        return render_template("/home.html")

    @app.route('/dashboard', strict_slashes=False)
    @login_required
    def dashboard_redirect():
        # Redirect to destination ports by default
        return redirect('/dashboard/destination-ports')

    # The dashboard pages are only accessible to authenticated users
    # via the @login_required decorator
    @app.route('/dashboard/destination-ports', methods=['POST', 'GET'])
    @login_required    # User must be authenticated
    def destination_ports_dashboard_page():
        # Render dashboard page and submit netflow record data
        global data_instance

        if request.method == 'POST':
            # User clicked time range button. Set cookie and reload page
            res = make_response(redirect('/dashboard/destination-ports'))
            time_range = request.form['time_range']
            res.set_cookie('timeRange', time_range.lower())
        else:
            monitored_ports_cookie = request.cookies.get('monitoredPorts')
            time_range_cookie = request.cookies.get('timeRange')
            # Start of dashboard session
            if data_instance is None:
                # Start of session but cookie was already set
                data_instance = Nfdump_data(time_range_cookie)
            elif time_range_cookie != data_instance.time_range:
                # Selected time range changed. Make new data set
                data_instance = Nfdump_data(time_range_cookie)

            # Build object with netflow data and summaries
            port_data = data_instance.get_dst_port_traffic()
            nfdump_data = {
                'in_dst_port_traffic': port_data[0],
                'out_dst_port_traffic': port_data[1],
                'longest_connections': data_instance.get_longest_connections(),
                'busiest_connections': data_instance.get_busiest_connections(),
                'port_alert_connections':
                    data_instance
                    .get_connections_with_matching_port(
                        monitored_ports_cookie),
            }
            res = make_response(
                render_template("data/dst_ports_dashboard.html",
                                nfdump_data=nfdump_data))
            if time_range_cookie is None:
                # If cookie not already set, set it to 'hour'
                res.set_cookie('timeRange', 'hour')

        return res

    @app.route('/dashboard/sources', methods=['POST', 'GET'])
    @login_required    # User must be authenticated
    def sources_dashboard_page():
        # Render dashboard page and submit netflow record data
        global data_instance

        if request.method == 'POST':
            # User clicked time range button. Set cookie and reload page
            res = make_response(redirect('/dashboard/sources'))
            time_range = request.form['time_range']
            res.set_cookie('timeRange', time_range.lower())
        else:
            monitored_ports_cookie = request.cookies.get('monitoredPorts')
            time_range_cookie = request.cookies.get('timeRange')
            # Start of dashboard session
            if data_instance is None:
                # Start of session but cookie was already set
                data_instance = Nfdump_data(time_range_cookie)
            elif time_range_cookie != data_instance.time_range:
                # Selected time range changed. Make new data set
                data_instance = Nfdump_data(time_range_cookie)

            # Build object with netflow data and summaries
            src_data = data_instance.get_src_addr_traffic()
            nfdump_data = {
                'in_src_addr_traffic': src_data[0],
                'out_src_addr_traffic': src_data[1],
                'longest_connections': data_instance.get_longest_connections(),
                'busiest_connections': data_instance.get_busiest_connections(),
                'port_alert_connections':
                    data_instance
                    .get_connections_with_matching_port(
                        monitored_ports_cookie),
            }
            res = make_response(render_template("data/sources_dashboard.html",
                                                nfdump_data=nfdump_data))
            if time_range_cookie is None:
                # If cookie not already set, set it to 'hour'
                res.set_cookie('timeRange', 'hour')

        return res

    @app.route('/dashboard/source-ports', methods=['POST', 'GET'])
    @login_required    # User must be authenticated
    def source_ports_dashboard_page():
        # Render dashboard page and submit netflow record data
        global data_instance

        if request.method == 'POST':
            # User clicked time range button. Set cookie and reload page
            res = make_response(redirect('/dashboard/source-ports'))
            time_range = request.form['time_range']
            res.set_cookie('timeRange', time_range.lower())
        else:
            monitored_ports_cookie = request.cookies.get('monitoredPorts')
            time_range_cookie = request.cookies.get('timeRange')
            # Start of dashboard session
            if data_instance is None:
                # Start of session but cookie was already set
                data_instance = Nfdump_data(time_range_cookie)
            elif time_range_cookie != data_instance.time_range:
                # Selected time range changed. Make new data set
                data_instance = Nfdump_data(time_range_cookie)

            # Build object with netflow data and summaries
            port_data = data_instance.get_src_port_traffic()
            nfdump_data = {
                'in_src_port_traffic': port_data[0],
                'out_src_port_traffic': port_data[1],
                'longest_connections': data_instance.get_longest_connections(),
                'busiest_connections': data_instance.get_busiest_connections(),
                'port_alert_connections':
                    data_instance
                    .get_connections_with_matching_port(
                        monitored_ports_cookie),
            }
            res = make_response(
                render_template("data/src_ports_dashboard.html",
                                nfdump_data=nfdump_data))
            if time_range_cookie is None:
                # If cookie not already set, set it to 'hour'
                res.set_cookie('timeRange', 'hour')

        return res

    @app.route('/dashboard/destinations', methods=['POST', 'GET'])
    @login_required    # User must be authenticated
    def destinations_dashboard_page():
        # Render dashboard page and submit netflow record data
        global data_instance

        if request.method == 'POST':
            # User clicked time range button. Set cookie and reload page
            res = make_response(redirect('/dashboard/destinations'))
            time_range = request.form['time_range']
            res.set_cookie('timeRange', time_range.lower())
        else:
            monitored_ports_cookie = request.cookies.get('monitoredPorts')
            time_range_cookie = request.cookies.get('timeRange')
            # Start of dashboard session
            if data_instance is None:
                # Start of session but cookie was already set
                data_instance = Nfdump_data(time_range_cookie)
            elif time_range_cookie != data_instance.time_range:
                # Selected time range changed. Make new data set
                data_instance = Nfdump_data(time_range_cookie)

            # Build object with netflow data and summaries
            dst_data = data_instance.get_dst_addr_traffic()
            nfdump_data = {
                'in_dst_addr_traffic': dst_data[0],
                'out_dst_addr_traffic': dst_data[1],
                'longest_connections': data_instance.get_longest_connections(),
                'busiest_connections': data_instance.get_busiest_connections(),
                'port_alert_connections':
                    data_instance
                    .get_connections_with_matching_port(
                        monitored_ports_cookie),
            }
            res = make_response(
                render_template("data/destinations_dashboard.html",
                                nfdump_data=nfdump_data))
            if time_range_cookie is None:
                # If cookie not already set, set it to 'hour'
                res.set_cookie('timeRange', 'hour')

        return res

    @app.route('/monitor-ports', methods=['POST', 'GET'])
    @login_required
    def monitor_ports():
        if request.method == 'POST':
            res = make_response(redirect('/dashboard/destination-ports'))

            # Convert all lists in form to tuples because lists are not
            # hashable
            monitored = [tuple(port) for port in loads(request.form['ports'])]

            # Remove all duplicate ports inside of monitored
            monitored = list(dict.fromkeys(monitored))

            res.set_cookie('monitoredPorts', dumps(monitored))
        else:
            monitored = request.cookies.get('monitoredPorts')

            # Nothing submitted
            if monitored is None:
                monitored = []
            else:
                monitored = loads(monitored)

            res = make_response(
                      render_template('data/monitor_form.html',
                                      monitored_ports=monitored))
        return res

    return app


# Start server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

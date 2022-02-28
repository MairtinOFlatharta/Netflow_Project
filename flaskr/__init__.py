from flask import Flask, render_template, make_response, request, redirect
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager

from .model import User, Nfdump_data


data_instance = None


def create_app():
    """ Flask application factory """

    # Setup Flask and load app.config
    app = Flask(__name__)

    # Config is external JSON file for now. Better than commiting keys
    app.config.from_json('../../application.json')

    # Setup Flask-MongoEngine
    db = MongoEngine(app)

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # The Home page is accessible to anyone
    @app.route('/')
    def home_page():
        # String-based templates
        return render_template("/home.html")

    # The dashboard page is only accessible to authenticated users
    # via the @login_required decorator
    @app.route('/dashboard', methods=['POST', 'GET'])
    @login_required    # User must be authenticated
    def dashboard_page():
        # Render dashboard page and submit netflow record data
        global data_instance

        if request.method == 'POST':
            # User clicked time range button. Set cookie and reload page
            res = make_response(redirect('/dashboard'))
            time_range = request.form['time_range']
            res.set_cookie('timeRange', time_range.lower())
        else:
            res = make_response(render_template("data/dashboard.html"))
            time_range_cookie = request.cookies.get('timeRange')
            # Start of dashboard session
            if data_instance is None:
                if time_range_cookie is None:
                    # Cookie wasn't set. Load default data within last hour
                    data_instance = Nfdump_data('hour')
                    # Set cookie
                    res.set_cookie('timeRange', 'hour')
                else:
                    # Start of session but cookie was already set
                    data_instance = Nfdump_data(time_range_cookie)
            elif time_range_cookie != data_instance.time_range:
                # Selected time range changed. Make new data set
                data_instance = Nfdump_data(time_range_cookie)
            # Just to test that data is being sent properly
            res.nfdump_data = data_instance.data.head()
        return res

    return app


# Start server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

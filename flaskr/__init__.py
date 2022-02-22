from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager

from .model import User


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
    @app.route('/dashboard')
    @login_required    # User must be authenticated
    def dashboard_page():
        # String-based templates
        return render_template("data/dashboard.html")

    return app


# Start server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

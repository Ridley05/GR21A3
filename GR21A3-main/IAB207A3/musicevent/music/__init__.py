from flask import render_template, Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True

    # We use this utility module to display forms quickly
    bootstrap = Bootstrap5(app)

    # Secret key for the session object
    app.secret_key = 'IAB207musicevent2023'

    # Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdb.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    #initialize the login manger
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    # Add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.evenbp)
    from . import auth
    app.register_blueprint(auth.authbp)
    
    app.register_error_handler(404, page_not_found)

    return app

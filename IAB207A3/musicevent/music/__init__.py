from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

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
    db.init_app(app)

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    # Add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import events
    app.register_blueprint(events.evenbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    return app
from flask import Blueprint, render_template

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    # events = events.query.all()
    return render_template('index.html')
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from music import create_app
# app = Flask(__name__)
# app.secret_key = 'IAB207musicevent2023'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventdb.sqlite'  # Change the database URI as needed
# db = SQLAlchemy(app)
app, db = create_app()

# Function to get the current date
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the User model for database storage
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    contact_number = db.Column(db.String(100))
    address = db.Column(db.String(200))
    events = db.relationship('Event', backref='user', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

# Define the Event model for database storage
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.String(100))
    status = db.Column(db.String(100))
    tickets_available = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='event', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookings = db.relationship('Booking', backref='event', lazy=True)

# Define the Comment model for database storage
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    comment = db.Column(db.Text)
    date_posted = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

# Define the Booking model for database storage
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    date = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

# Landing page
@app.route('/')
def landing_page():
    upcoming_events = Event.query.all()
    return render_template('landing.html', events=upcoming_events)
#
# # Login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email, password=password).first()
#         if user:
#             session['user_id'] = user.id
#             return redirect(url_for('landing_page'))
#         else:
#             error = 'Invalid email or password. Please try again.'
#             return render_template('login.html', error=error)
#     return render_template('login.html')
#
# # Logout
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('landing_page'))

# Event details page
@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get(event_id)
    return render_template('event_details.html', event=event)
#
# # Registration page
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         new_user = User(
#             name=request.form['name'],
#             email=request.form['email'],
#             password=request.form['password'],
#             contact_number=request.form['contact'],
#             address=request.form['address']
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

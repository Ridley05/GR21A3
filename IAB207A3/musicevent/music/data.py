from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'IAB207musicevent2023'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db' 
db = SQLAlchemy(app)

# Function to get the current date
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define the User model for database storage
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    events = db.relationship('Event', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='booker', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)

# Define the Event model for database storage
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.String(100))
    tickets_available = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='event', lazy=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(100))

# Define the Comment model for database storage
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text)
    date_posted = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    events = Event.query.all()
    return render_template('index.html', events=events)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('landing_page'))
        else:
            return render_template('login.html', error='Invalid username or password. Please try again.')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('landing_page'))

# Event details page
@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get(event_id)
    comments = Comment.query.filter_by(event_id=event_id).all()
    return render_template('event.html', event=event, comments=comments)

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('landing_page'))
    return render_template('register.html')

# Event creation page
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        tickets_available = int(request.form['tickets_available'])
        user_id = session['user_id']
        status = 'Open'
        event = Event(name=name, description=description, date=date, tickets_available=tickets_available, user_id=user_id, status=status)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('landing_page'))
    return render_template('create_event.html')

# Comment creation
@app.route('/event/<int:event_id>/comment', methods=['POST'])
def create_comment(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        comment_text = request.form['comment_text']
        date_posted = get_current_date()
        user_id = session['user_id']
        comment = Comment(comment_text=comment_text, date_posted=date_posted, event_id=event_id, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('event_details', event_id=event_id))

# Booking creation
@app.route('/event/<int:event_id>/book', methods=['POST'])
def create_booking(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        event = Event.query.get(event_id)
        if event.tickets_available >= quantity:
            event.tickets_available -= quantity
            db.session.add(event)
            user_id = session['user_id']
            price = quantity * 100  # Price per ticket could be stored in the Event, but for this example let's say it's 100
            date = get_current_date()
            booking = Booking(price=price, quantity=quantity, date=date, user_id=user_id, event_id=event_id)
            db.session.add(booking)
            db.session.commit()
            return redirect(url_for('event_details', event_id=event_id))
        else:
            return render_template('event.html', event=event, error='Not enough tickets available.')




with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


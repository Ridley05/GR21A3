from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	# Password is encrypted and stored
	# Storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # Relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(400))
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    venue = db.Column(db.String(80))
    eventtype = db.Column(db.String(30))
    description = db.Column(db.String(200))
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    ticketnumber = db.Column(db.Integer)
    ticketprice = db.Column(db.Float(80))
    ticketlimit = db.Column(db.Integer)

    # Create the Comments db.relationship
	# Relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
	
    def __repr__(self): # String print method
        return "<Name: {}>".format(self.name)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # Add foreign key relations for each user and each music event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
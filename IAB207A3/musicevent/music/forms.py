from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}
TYPE_OF_EVENT = {'Livehouse', 'Musical', 'Concert', 'Festival'}                               

#Create new event
class EventForm(FlaskForm):
  image = FileField('Upload a picture for your new event!', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  eventname = StringField('Event Name', validators=[InputRequired()])
  venue = StringField('Venue', validators=[InputRequired()])
  eventtype = SelectField(choices = TYPE_OF_EVENT, label = 'Type of Event', validators=[InputRequired()])
  description = TextAreaField('Description of Event', validators=[InputRequired()])
  date = DateField('Date', validators=[InputRequired()])
  time = TimeField('Time Open for Booking')
  ticketnumber = IntegerField('Capacity of Audience', validators=[InputRequired()])
  ticketprice = IntegerField('Price of Tickets Sold', validators=[InputRequired()])
  ticketlimit = IntegerField('Limitation Purchase Per Account', validators=[NumberRange(min=1, max=5, message='Pick between 1 to 5')])
  submit = SubmitField("Submit to Create")
  cancel = SubmitField("Cancel to Exit")
    
#User login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired("Write a comment")])
  submit = SubmitField('Create')
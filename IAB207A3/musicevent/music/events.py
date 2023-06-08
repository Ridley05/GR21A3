from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename

evenbp = Blueprint('event', __name__, url_prefix='/events')

@evenbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm()    
    return render_template('events/show.html', event=event, form=cform)

@evenbp.route('/create', methods=['GET', 'POST'])
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    # User pressed 'Submit to Create'
    if form.submit.data:
       # Call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(image = db_file_path, 
                      name = form.name.data,
                      venue = form.venue.data, 
                      eventtype = form.eventtype.data,
                      description = form.description.data, 
                      date = form.date.data,
                      time = form.time.data, 
                      ticketnumber = form.ticketnumber.data,
                      ticketprice = form.ticketprice.data, 
                      ticketlimit = form.ticketlimit.data)
        # Add the object to the db session
        db.session.add(event)
        # Commit to the database
        db.session.commit()
        print('Successfully created new music event', 'success')
        # Always end with redirect when form is valid
        return redirect(url_for('event.create'))
    # User pressed 'Cancel to Exit'
    else:
       return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)


def check_upload_file(form):
  # Get file data from form  
  fp = form.image.data
  filename = fp.filename
  # Get the current path of the module file, store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # Upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  # Store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  # Save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@evenbp.route('/<event>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    # Get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==event))
    if form.validate_on_submit():  
      # Read the comment from the form
      comment = Comment(text=form.text.data, event=event) 
      # Back-referencing works, comment.event is set, link is created
      db.session.add(comment) 
      db.session.commit() 

      # Flash message handled by the html
      # Flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # Using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=event.id))
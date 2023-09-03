from flask import Blueprint, render_template, request, flash, jsonify, redirect, request
from flask_login import login_required, current_user
from datetime import datetime
from .models import Events, Comment, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    events = Events.query.all()
    if request.method == 'POST':
        print("Redirect to create event")

    return render_template("home.html", user=current_user, events=events)

@views.route("/event/<int:event_id>", methods=['GET', 'POST'])
@login_required
def show_event(event_id):
    event = Events.query.get(event_id)
    comments = Comment.query.filter_by(event_id=event_id).all()
    commentators = {}
    for comment in comments:
        buff_comment = User.query.filter_by(id=comment.user_id).all()
        commentators[comment.user_id] = buff_comment[0].first_name
    print(commentators)
    participants = event.participants
    participant_names = [participant.first_name for participant in participants]
    if request.method == 'POST':
        new_comment = Comment(description=request.form.get('comment'), date=datetime.utcnow(), user=current_user, event=event)
        if new_comment.description != '':
            db.session.add(new_comment)
            db.session.commit()
            comments = Comment.query.filter_by(event_id=event_id).all()
            return render_template("event.html", user=current_user, event=event, 
                            participants=participant_names, comments=comments, commentators=commentators)
    return render_template("event.html", user=current_user, event=event, 
                           participants=participant_names, comments=comments, commentators=commentators)

@views.route('/createevent', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        name = request.form.get('namevent')
        description = request.form.get('eventdescription')
        date1 = request.form.get('date')
        date2 = request.form.get('time')
        date = datetime.strptime(date1 + ' ' + date2, '%Y-%m-%d %H:%M')
        place = request.form.get('where')
        # Mettre les contraintes ici
        new_event = Events(name=name, description=description, 
                           organizer_id=current_user.id, date=date,
                           place=place)
        db.session.add(new_event)
        db.session.commit()
        new_event.participants.append(current_user)
        db.session.commit()
        return redirect("/")

    return render_template("createEvent.html", user=current_user)


@views.route('/delete-event', methods=['POST'])
def delete_event():  
    event = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    eventId = event['eventId']
    event = Events.query.get(eventId)
    if event:
        if event.organizer_id == current_user.id:
            db.session.delete(event)
            db.session.commit()

    return jsonify({})

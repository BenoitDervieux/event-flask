from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from datetime import datetime
from .models import Note, Events
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
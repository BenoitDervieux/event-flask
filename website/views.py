from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Note, Events
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        print("Redirect to create event")

    return render_template("home.html", user=current_user)

@views.route('/createevent', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        name = request.form.get('namevent')
        description = request.form.get('eventdescription')
        date = request.form.get('date')
        place = request.form.get('where')
        # Mettre les contraintes ici
        new_event = Events(name=name, description=description, 
                           organizer_id=current_user.id, date=date,
                           place=place)
        return redirect("/")

    return render_template("createEvent.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

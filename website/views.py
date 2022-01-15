from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json 
from datetime import date

views = Blueprint('views', __name__)

@views.route('/',  methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.form.get('note')
        note  = Note.query.filter_by(data=data).first()


        if note:
            flash('Note already exists', category='error')
        elif len(data) < 1:
            flash('Note has to contain at least one character', category = 'error')
        else:

            new_note = Note(data = data, user_id = current_user.id)
            current_user.no_notes += 1
            db.session.add(new_note)
            db.session.commit()

            flash('Note added', category='success')










    return render_template("home.html", user = current_user)

@views.route('/delete-note',  methods=['POST'])
def deletenote():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            current_user.no_notes -= 1;
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted', category='error')
            
    return jsonify({})


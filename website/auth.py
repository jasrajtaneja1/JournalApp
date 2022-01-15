import re
from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password =  request.form.get('password')

        user  = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('You have succesfully logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

                
            else:
                flash('Invalid login', category='error')
        else:
            flash('Account does not exist', category='error')

  
    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/profile', methods= ['GET', 'POST'])
@login_required
def profile():

    if request.method == 'POST':
        insta_username = request.form.get('insta_username')
        twitter_username = request.form.get('twitter_username')
        about_me = request.form.get('about_me')
        email = request.form.get('email')
        validate = 0
       

        if email!=current_user.email:
             user1  = User.query.filter_by(email = email).first()
             if user1:
                 validate = 1
                 flash("That email is taken", category='error')
        if validate!=1:
            if len(email) == 0:
                email = current_user.email
                current_user.email = email
                db.session.commit()
            if len(twitter_username) == 0:
                twitter_username = current_user.twitter_username
                current_user.twitter_username = twitter_username
                db.session.commit()
            if len(insta_username) == 0:
                insta_username = current_user.insta_username
                current_user.insta_username = insta_username
                db.session.commit()
            if len(about_me) == 0:
                about_me = current_user.about_me
                current_user.about_me = about_me
                db.session.commit()    
            


        
            if len(about_me)>150:
                flash('Bio cannot be more than 150 characters', category='error')
            else:
                current_user.insta_username = insta_username
                current_user.twitter_username = twitter_username
                current_user.about_me = about_me
                current_user.email = email
                db.session.commit()
                flash("Account settings successfully updated!", category='success')
                return redirect(url_for('auth.profile'))
        
       
    
        
    return render_template("profile.html", user = current_user)
    

@auth.route('/search', methods = ['GET', 'POST'])
def search():
    return "<h1> coming soon......this feature will allow you to search other users profiles and view them </h1"



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if request.method == 'POST':
        email =  request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user  = User.query.filter_by(email = email).first()


        if user:
            flash('Email already exists', category='error')
    

        elif len(email) < 3:
            flash('Email must be greater than 2 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than one character', category='error')
        elif(password1 != password2):
            flash('passwords do not match', category='error')
        elif len(password1) < 6:
            flash('password must be greater than 5 characters', category='error')
    

        else:
            new_user = User(email=email, no_notes = 0, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
        
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account succesfully created', category='success')
           

            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)

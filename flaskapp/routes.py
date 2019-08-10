
from flask import request, redirect, render_template, url_for, flash
from flaskapp.models import User, Word
from flaskapp import db, bcrypt, app
from flaskapp.api import information
from flaskapp.forms import LoginForm, RegistrationForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.imagegen import generate_url, white_screen, blue_gradient

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        try:
            input_word = request.args.get('word')
            word_meaning = information(input_word)
            if current_user.is_authenticated:
                looking_word = Word.query.filter_by(user_id=current_user.id, word=input_word).first()
                if (looking_word != None):
                    looking_word.time = datetime.utcnow()
                    looking_word.searched += 1
                    db.session.add(looking_word)
                    db.session.commit()
                else:
                    word = Word(word=input_word, user_id=current_user.id, searched=1)
                    db.session.add(word)
                    db.session.commit()
            else:
                flash("Your words will not be saved. Login or Sign Up to save words", 'info')
            return render_template('search.html', word=word_meaning, name="search", background_url=generate_url())
        except:
            return redirect(url_for("error"))

@app.route("/error", methods=["GET", "POST"])
def error():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template("error.html", name="error", background_url=generate_url())
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash("Login Successful. Welcome 😄", 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unccessful. Please check username and password", 'danger')
    return render_template("login.html", name="login", form=form, background_url=blue_gradient())

@app.route("/")
@app.route("/home", methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('home.html', name="home", background_url=white_screen())

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, and now you can login 👍", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", name="register", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', "POST"])
@login_required
def account():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('account.html', name="account", background_url=white_screen())

@app.route("/view")
@login_required
def view():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('view.html', name='view', background_url=generate_url())
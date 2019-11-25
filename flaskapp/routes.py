
from flask import request, redirect, render_template, url_for, flash, jsonify
from flaskapp.models import User, Word
from flaskapp import db, bcrypt, app
from flaskapp.api import extract
from flaskapp.forms import LoginForm, RegistrationForm, AccountForm
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.imagegen import generate_url, white_screen, blue_gradient
from flaskapp.SRS import new_time
from ast import literal_eval


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        try:
            input_word = request.args.get('word')
            word_meaning = extract(input_word).compile_json()
            if current_user.is_authenticated:
                looking_word = Word.query.filter_by(
                    user_id=current_user.id, word=input_word).first()
                if (looking_word != None):

                    looking_word.time = datetime.utcnow()
                    looking_word.level = 1 if looking_word.level == 1 or looking_word.level == 0 else looking_word.level//2

                    looking_word.due_date = new_time(
                        datetime.utcnow(), looking_word.level)
                    db.session.add(looking_word)
                    db.session.commit()
                else:
                    word = Word(word=input_word, user_id=current_user.id,
                                due_date=new_time(datetime.utcnow(), 1), level=1)
                    db.session.add(word)
                    db.session.commit()
            else:
                flash(
                    "Your words will not be saved. Login or Sign Up to save words", 'info')
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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data.encode('utf-8'))
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
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
    form = AccountForm()
    if form.validate_on_submit():
        user = current_user
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if (form.username.data != ""):
                user.username = form.username.data
            if (form.email.data != ""):
                user.email = form.email.data

            db.session.add(user)
            db.session.commit()
            flash("Change Successful")
            return redirect(url_for('home'))
        else:
            flash("Change Unccessful. Please check password", 'danger')
    return render_template("login.html", name="login", form=form, background_url=blue_gradient())
    '''form = AccountForm()
    if form.validate_on_submit():
        user = current_user
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if (form.username.data != ""):
                user.username = form.username.data
            if (form.email.data != ""):
                user.email = form.email.data

            db.session.add(user)
            db.session.commit()
            flash("Change Successful")
            return redirect(url_for('home'))
        else:
            flash("Change Unccessful. Please check password", 'danger')
    return render_template("login.html", name="login", form=form, background_url=blue_gradient())'''
    return render_template("account.html", name="account", form=form)


@app.route("/view", methods=['GET', 'POST'])
@login_required
def view():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('view.html', name='view', background_url=generate_url())


@app.route("/practice")
@login_required
def practice():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        user_words = User.query.get(current_user.id).words
        due_today = []
        for word in user_words:
            if (word.due_date.date() <= datetime.today().date()):
                due_today.append(word)
        return render_template('practice.html', name='practice', background_color="rgb(52,58,64)", words_due_today=due_today, js_file="practice.js")


@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    if (request.method == 'POST'):
        jsdata = request.get_json()
        return redirect(url_for('review', data=jsdata))
    else:
        inpjsdata = literal_eval(request.args.get('data'))
        words_to_review = {}
        for key, value in inpjsdata.items():
            current_word = Word.query.filter_by(
                user_id=current_user.id, word=key).first()
            current_word.time = datetime.utcnow()
            if (value == 1):
                current_word.level = current_word.level + 1
            else:
                words_to_review[key] = extract(key).compile_json
            current_word.due_date = new_time(
                current_word.time, current_word.level)

            db.session.add(current_word)
            db.session.commit()

        return render_template("review.html", data=words_to_review, name="review", background_url=generate_url())

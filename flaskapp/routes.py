
from flask import request, redirect, render_template, url_for, flash
from flaskapp.models import User
from flaskapp import db, bcrypt, app
from flaskapp.api import information
from flaskapp.forms import LoginForm, RegistrationForm
from flask_login import login_user

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        try:
            input_word = information(request.args.get('word'))
            return render_template('search.html', word=input_word, name="search")
        except:
            return redirect(url_for("error"))

@app.route("/error", methods=["GET", "POST"])
def error():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template("error.html", name="error")
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login Unccessful. Please check username and password", 'danger')
    return render_template("login.html", name="login", form=form, background_url="https://webgradients.com/public/webgradients_png/019%20Malibu%20Beach.png")

@app.route("/")
@app.route("/home", methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        output_word = request.form['search_word']
        return redirect(url_for('search', word=output_word))
    else:
        return render_template('home.html', name="home", background_url="https://i.ytimg.com/vi/YC5WrEArgxY/maxresdefault.jpg")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, and now you can login", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", name="register", form=form)

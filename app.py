from flask import Flask, render_template, request, url_for, redirect, flash
from api import information
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    words = db.relationship('Word', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(45), unique=True, nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Word('{self.word}', '{self.time}', '{self.user_id}')"

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
        if form.username.data == "udaygoyat45" and form.password.data == "udaygoyat#4":
            flash("You are now logged in", 'success')
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
        user = User(username=form.username.data, email=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Your account has been created, and now you can login", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", name="register", form=form)

if (__name__ == "__main__"):
    app.run(debug=True)

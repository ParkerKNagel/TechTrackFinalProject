from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Column
import json
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_login import login_required

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

login_manager = LoginManager()

login_manager.init_app(app)

bcrypt = Bcrypt(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/GameDatabase"
app.config['SECRET_KEY'] = "Don't"

db.init_app(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    publisher = db.Column(db.String())
    console = db.Column(db.String())
    genre = db.Column(db.String())
    rating = db.Column(db.String(20))
    score = db.Column(db.String(3))
    # This is the code that creaetes the class of games that the database gets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
#this is the same thing but it is for the creation of users

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('base.html', game=Game)
#this is the route to the home page

@app.route('/create_game', methods=["GET", "POST"])
@login_required
def create_game():
    if request.method == "POST":
        game = Game(
            title=request.form["title"],
            publisher=request.form["publisher"],
            console=request.form["console"],
            genre=request.form["genre"],
            rating=request.form["rating"],
            score=request.form["score"],
        )
        db.session.add(game)
        db.session.commit()
    return render_template("add.html")
#this is the route for adding games to the database

@app.route('/index')
def index():
    games = Game.query.all()  # Fetch all games from the database
    return render_template('index.html', games=games)
#this is the route for getting to the list of all the games

@app.route('/sort/<attribute>')
def sort(attribute):
    valid_attributes = ['title', 'publisher', 'console', 'genre', 'rating', 'score']

    if attribute in valid_attributes:
        # Sort by the chosen attribute
        attr = getattr(Game, attribute)

        # Fetch all games from the database
        games = Game.query.all()

        # Check if the attribute requires a reversed order
        reverse_order = request.args.get('reverse', '').lower() == 'true'
        if reverse_order:
            sorted_games = sorted(games, key=lambda x: getattr(x, attribute), reverse=True)
        else:
            sorted_games = sorted(games, key=lambda x: getattr(x, attribute))

        return render_template('index.html', games=sorted_games)
    else:
        return "Invalid attribute"  # Handle invalid attribute
#this is the code that deals with the sorting of the games in index.html

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
#this is the route for logging out

@app.route('/register', methods=['GET', 'POST'])
def  register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username,password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to base.html after registration
    return render_template('registration.html')
#this is the route for making a new account

@app.route('/login', methods=['GET', 'POST'])
def  login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        print(password)
        print(user.password_hash)
        print(bcrypt.check_password_hash(user.password_hash, password))

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))  # Redirect to base.html after login
    return render_template('login.html')
#this is the route for making a new account

if __name__ == '__main__':
    app.run(debug=True)
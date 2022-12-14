from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///study-buddy-app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --Study Session
class Study_Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    location = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    signed_up = db.Column(db.Boolean, default=False)

# --User
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

db.create_all()





def read_not_signed_up_session():
    return Study_Session.query.filter_by(signed_up=False).all()

def read_signed_up_session():
    return Study_Session.query.filter_by(signed_up=True).all()


@app.route("/")
def welcome():
    return render_template("home.html")


@app.route("/main")
def main():
    print('running this one')
    if not session.get("username"):
        
        return render_template("main.html")
    else:
        return redirect(url_for('home'))
    

@app.route("/home")
def home():
    # read study sessions from db
    if not session.get('username'):
        return redirect(url_for('main'))
    print("rendering home")
    username = session['username']
    study_sesison_list = read_not_signed_up_session()
    signed_up_session_list = read_signed_up_session()
    return render_template("index.html", study_session_list=study_sesison_list, username=username, signed_up_session_list=signed_up_session_list)

@app.route("/create_study_session")
def create_study_session():
        return render_template("create-session.html")

@app.route("/add_study_session", methods=['POST'])
def add_study_session():
    print('username:', session['username'])
    # logout -> delete username from dictionary (new route with logout)

    new_study_session = Study_Session(
        subject = request.form['subject'],
        date = datetime.strptime(request.form['session_date'], "%Y-%m-%d"),
        start_time = request.form['start_time'],
        end_time=request.form['end_time'],
        location = request.form['location'],
        description = request.form['description']
    )
    db.session.add(new_study_session)
    db.session.commit()
    return redirect(url_for('home'))

#######################
#### Session Management
#######################
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")



@app.route("/login", methods=["POST", "GET"])
def login():
    print(
    'running login'
    )
    if request.method == "POST":
        session["StudySessionID"] = request.form.get("StudySessionID")
        username = request.form.get('Username')
        password = request.form.get('password')
        data = request.form['Login']
        session['username'] = username

        #TODO: Check if it is a valid username or not

        return redirect(url_for('home'))

    print('not a post')
    if session['username']:
        return 'Your username is '+session['username']
    return render_template("login.html")

@app.route("/sign_up")
def sign_up():
    session_id = request.args.get("session_id")

    selected_session = Study_Session.query.get(session_id)
    selected_session.signed_up = True
    db.session.commit()

    return redirect(url_for('home'))

@app.route("/signin")
def signin():
    return render_template("signin.html")

if __name__ == '__main__':
    app.run(debug=True)

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
    # TODO: add who created
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    location = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=True)

# --User
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), nullable=False)

db.create_all()





def read_study_session():
    return db.session.query(Study_Session).all()


@app.route("/")
def main():
    if not session.get("StudySessionID"):
        
        return render_template("main.html")
    else:
        return redirect(url_for('home'))
    


@app.route("/")
def home():
    # read study sessions from db
    study_sesison_list = read_study_session()
    return render_template("index.html", study_session_list=study_sesison_list)

@app.route("/create_study_session")
def create_study_session():
    if not session.get("StudySessionID"):
        return redirect(url_for('home'))
    else:
        return render_template("create-session.html")

@app.route("/add_study_session", methods=['POST'])
def add_study_session():
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
    if request.method == "POST":
        session["StudySessionID"] = request.form.get("StudySessionID")

        #TODO: Check if it is a valid username or not
        return redirect(url_for('home'))
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///study-buddy-app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --Study Session
class Study_Session(db.Model):
    # TODO: add who created
    id=db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(250), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=True)

db.create_all()

def read_study_session():
    return db.session.query(Study_Session).all()

@app.route("/")
def home():
    # read study sessions from db
    study_sesison_list = read_study_session()
    return render_template("index.html", study_session_list=study_sesison_list)

@app.route("/create_study_session")
def create_study_session():
    return render_template("create-session.html")

@app.route("/add_study_session", methods=['POST'])
def add_study_session():
    print(type(request.form['date_time']), request.form['date_time'])
    new_study_session = Study_Session(
        subject = request.form['subject'],
        date_time = datetime.strptime(request.form['date_time'], "%Y-%m-%dT%H:%M"),
        location = request.form['location'],
        description = request.form['description']
    )
    db.session.add(new_study_session)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

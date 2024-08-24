from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    id= db.Column(db.String(20))
    gender=db.Column(db.String(1))
    age = db.Column(db.Integer)

    emo_competence = db.Column(db.Integer)
    emo_joy = db.Column(db.Integer)
    emo_pride = db.Column(db.Integer)
    emo_boredom = db.Column(db.Integer)
    emo_irritation = db.Column(db.Integer)
    emo_anxiety = db.Column(db.Integer)
    emo_shame = db.Column(db.Integer)


    feedback = db.Column(db.String(1000))
    station_track = db.Column(db.String(500), nullable=True)
    result = db.Column(db.String(50), nullable=True)
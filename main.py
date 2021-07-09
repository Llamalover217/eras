from flask import Flask, render_template, g, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///facts.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Greek(db.Model):
    __tablename__ = 'greek'

    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.Text)

class Hellenistic(db.Model):
    __tablename__ = 'hellenistic'

    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.Text)

class Roman(db.Model):
    __tablename__ = 'roman'

    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.Text)

class Random(db.Model):
    __tablename__ = 'random'

    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.ForeignKey('Greek.id'))
    rid = db.Column(db.ForeignKey('Roman.id'))
    hid = db.Column(db.ForeignKey('Hellenistic.id'))

@app.route("/")
@app.route("/home")
def home():
  print(random.randrange(1,10))
  return render_template('home.html', GreekEra=Greek.query.all(), HellenisticEra=Hellenistic.query.all(), RomanEra=Roman.query.all(), RandomEra=Random.query.all())

@app.route("/greek")
def greek():
  return render_template('greek.html')

@app.route("/hellenistic")
def hellenistic():
  return render_template('hellenistic.html')

@app.route("/roman")
def roman():
  return render_template('roman.html')

@app.route('/greek_api/<int:id>')
def greek_api(id):       # defines the greek fact choosen
    GreekEra = Greek.query.get_or_404(id)
    return render_template('greek_fact.html', GreekEra=GreekEra)

@app.route('/roman_api/<int:id>')
def roman_api(id):       # defines the greek fact choosen
    RomanEra = Roman.query.get_or_404(id)
    return render_template('roman_fact.html', RomanEra=RomanEra)

@app.route('/hellenistic_api/<int:id>')
def getHellenistic(id):
    HellenisticEra = Hellenistic.query.get_or_404(id)
    return render_template('hellenistic_fact.html', HellenisticEra=HellenisticEra)

@app.route('/random_api/<int:id>')
def getRandom(id):
    RandomEra = Random.query.get_or_404(id)
    return render_template('random_fact.html', RandomEra=RandomEra, GreekEra=Greek.query.all(), HellenisticEra=Hellenistic.query.all(), RomanEra=Roman.query.all())

if __name__ == "__main__":
  app.run(debug=True)
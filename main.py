from flask import Flask, render_template, g, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///facts.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

association = db.Table('era_fact_mapping', 
    db.Column('era_id', db.ForeignKey('era.id')),
    db.Column('fact_id', db.ForeignKey('fact.id'))
)

class Era(db.Model):
    __tablename__ = 'era'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    facts = db.relationship('Fact', secondary=association, backref='Fact')

class Fact(db.Model):
    __tablename__ = 'fact'

    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.Text)
    eras = db.relationship('Era', secondary=association, backref='Era')

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
@app.route("/home")   # links to home page
def home():
  return render_template('home.html', GreekEra=Greek.query.all(), HellenisticEra=Hellenistic.query.all(), RomanEra=Roman.query.all(), RandomEra=Random.query.all())

@app.route("/greek")  # links to greek page
def greek():
  return render_template('greek.html')

@app.route("/hellenistic")    # links to hellenistic page
def hellenistic():
  return render_template('hellenistic.html')

@app.route("/roman")    # links to roman page
def roman():
  return render_template('roman.html')

# @app.route('/facts')
# def facts_all_api():       # defines random fact choosen
#     # Fact = Greek.query.get_or_404(id)
#     stmt = (
#       db.select(Fact).
#       join(Fact.eras)
#     )
#     myFacts = db.session.execute(stmt).all()
#     myFact = random.choice(myFacts)
#     myFactDesc = myFact.fact
#     myEras = 'XXXX'
#     # to do: pull out random from list myFacts
#     return render_template('fact.html', Era=myEras, Fact=myFactDesc)

@app.route('/facts/<string:name>')
def facts_api(name):       # defines random fact choosen
    myFacts = db.session.query(Fact.fact).filter(Fact.eras.any(Era.name == name)).all()

    myFact = random.choice(myFacts)
    # to do: pull out random from list myFacts
    return render_template('fact.html', Era=name, Fact=myFact)

@app.route('/random_api/<int:id>')
def getRandom(id):        # defines the random fact choosen
    RandomEra = Random.query.get_or_404(id)
    GreekEra = Greek.query.get_or_404(id)
    RomanEra = Roman.query.get_or_404(id)
    HellenisticEra = Hellenistic.query.get_or_404(id)
    return render_template('random_fact.html', RandomEra=RandomEra, GreekEra=GreekEra, RomanEra=RomanEra, HellenisticEra=HellenisticEra)

if __name__ == "__main__":
  app.run(debug=True)
from flask import Flask, render_template, g, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/greek")
def greek():
  return render_template('greek.html')

@app.route("/hellenistic")
def hellenistic():
  return render_template('hellenistic.html')

@app.route("/roman")
def roman():
  return render_template('roman.html')

if __name__ == "__main__":
  app.run(debug=True)
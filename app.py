from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acpeltol"
db = SQLAlchemy(app) 

# Routes to different pages!


#Main page

@app.route("/", methods = ["POST", "GET"])
def index():
     
    if request.method == "POST":
        print(request.form["uname"])
        print(request.form["upass"])

    print(db.session.execute(text('SELECT * FROM hulio')).fetchall())
    return render_template("base.html")

@app.route("/page1")
def page1():

    return render_template("register_page.html")

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"
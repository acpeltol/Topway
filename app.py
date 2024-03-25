from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acpeltol"
db = SQLAlchemy(app) 

# Routes to different pages!

# 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


def new_user_check(uname, upass):
    return

#Main page

@app.route("/", methods = ["POST", "GET"])
def index():

    texto = ""
     
    #Checks if username and password is correct 

    if request.method == "POST":

        u_id = db.session.execute(text(f'''SELECT id FROM users
                                   WHERE uname = '{request.form["uname"]}' AND upass = '{request.form["upass"]}' ''')).fetchall()
            
        print(u_id)

        print(request.form["uname"])

        print(request.form["upass"])

        if len(u_id) == 1:
            return "Hello kioto"
    
        else:
            texto = "Username or paswors is wrong"

    print(db.session.execute(text('SELECT * FROM hulio')).fetchall())
    return render_template("base.html", texto = texto)


# REGISTER PAGE

@app.route("/register", methods = ["POST", "GET"])
def register():

    if request.method == "POST":
        
        result = new_user_check(request.form["runame"],request.form["rupass"])
        
        #db.session.execute(text('SELECT * FROM hulio'))

    return render_template("register_page.html")

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"
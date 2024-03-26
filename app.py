from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acpeltol"
db = SQLAlchemy(app) 

# Routes to different pages!

# Checks if new users username exists

def new_user_check(uname, upass):

    if uname == "" or upass == "":
        return "Wrog type of name or password"
    
    u_id = db.session.execute(text(f'''SELECT id FROM users WHERE uname = '{uname}' ''')).fetchall()
    
    print(u_id)

    if len(u_id) == 1:        
        return "Username alredy exists"


    return "gato"

#Main page

@app.route("/", methods = ["POST", "GET"])
def index():

    texto = ""
     
    #Checks if username and password is correct 

    if request.method == "POST":

        u_id = db.session.execute(text(f'''SELECT id FROM users
                                   WHERE uname = '{request.form["uname"]}' AND upass = '{request.form["upass"]}' ''')).fetchall()
            
        #print(u_id)

        #print(request.form["uname"])

        #print(request.form["upass"])

        if len(u_id) == 1:
            return "Hello kioto"
    
        else:
            texto = "Username or paswors is wrong"

    print(db.session.execute(text('SELECT * FROM hulio')).fetchall())
    return render_template("base.html", texto = texto)

# REGISTER PAGE

@app.route("/register", methods = ["POST", "GET"])
def register():

    texto_register = ""

    if request.method == "POST":
        
        texto_register = new_user_check(request.form["runame"],request.form["rupass"])

        if texto_register == "gato":

            db.session.execute(text(f'''INSERT INTO users (uname, upass) VALUES ('{request.form["runame"]}', '{request.form["rupass"]}')'''))
            db.session.commit()

            print("hulio")


    return render_template("register_page.html", texto_register = texto_register)

@app.route("/page2")
def page2():
    return "Tämä on sivu 2"
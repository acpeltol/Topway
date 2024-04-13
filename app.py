from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.secret_key = "Alejandro"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///acpeltol"
db = SQLAlchemy(app)

# Functions which checsk parameters and lead to right pages

# Checks if new users username exists and if it has correct type password

def new_user_check(uname, upass):

    # If user types nothing then it rejects sign up
    
    if uname == "" or upass == "":
        return "Wrog type of name or password"
    
    # If password has not uppercase letters then it rejects password

    if upass == upass.lower():
        return "Password must have at least one capital letter"
    
    # If password is too short it rejects password

    if len(upass) < 8:
        return "Your password must be at least 8 charecters long"
    
    # If username alredy exists it rejects username

    u_id = db.session.execute(text(f'''SELECT id FROM users WHERE uname = '{uname}' ''')).fetchall()

    if len(u_id) == 1:        
        return "Username alredy exists"


    return 1

#Routes to different pages

#Opening page

@app.route("/", methods = ["POST", "GET"])
def index():

    texto = ""
     
    #Checks if username and password is correct 

    if request.method == "POST":

        u_id = db.session.execute(text(f'''SELECT id,upass  FROM users
                                   WHERE uname = '{request.form["uname"]}' ''')).fetchall()

        print(u_id)            

        if len(u_id) != 1:            
            
            texto = "Username is wrong"
            return render_template("base.html", texto = texto)
    
        if check_password_hash(u_id[0][1], request.form["upass"]):

            user = request.form["uname"]
            session["user"] = user

            return render_template("main_page.html", texto = session["user"])
        
        else:

            texto = "Password is wrong"
            return render_template("base.html", texto = texto)

    return render_template("base.html", texto = texto)

# REGISRATION PAGE

@app.route("/register", methods = ["POST", "GET"])
def register():

    texto_register = ""

    # If user writes down the name and the password it will go next statement

    if request.method == "POST":
        
        texto_register = new_user_check(request.form["runame"],request.form["rupass"])

        if texto_register == 1:

            db.session.execute(text(f'''INSERT INTO users (uname, upass) VALUES ('{request.form["runame"]}', '{generate_password_hash(request.form["rupass"])}')'''))
            db.session.commit()

            user = request.form["runame"]
            session["user"] = user

            return render_template("main_page.html",texto = session["user"])



    return render_template("register_page.html", texto_register = texto_register)

@app.route("/main_pgae", methods = ["POST", "GET"])
def main_page():
    return 

@app.route("/get_information", methods = ["POST", "GET"])
def get_information():
    return render_template("register_page.html")
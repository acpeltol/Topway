from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

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

# Checks if new user's information was put right

def new_users_information_check(fname,lname,bday):

    date = datetime.datetime.now()

    print(bday[8:10])

    if fname == "":
        return "Write your name"
    
    if lname == "":
        return "Write your lastname"
    
    if bday == "":
        return "Please give us your birthday"
    
    if int(bday[0:4]) > date.year:
        return "This year hasn't comen yet"
    
    if int(bday[0:4]) == date.year and int(bday[5:7]) > date.month:
        return "This month of this year hasn't commen yet"
    
    if int(bday[0:4]) == date.year and int(bday[5:7]) == date.month and int(bday[8:10]) > date.day:
        return "This day of this month hasn't commen yet"

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

        if len(u_id) != 1:            
            
            texto = "Username is wrong"
            return render_template("base.html", texto = texto)
    
        if check_password_hash(u_id[0][1], request.form["upass"]):

            user = request.form["uname"]
            session["user"] = user

            u_id = db.session.execute(text(f'''  
                    SELECT * FROM users_information WHERE user_name = '{session["user"]}' ''')).fetchall()
            
            if len(u_id) == 1:
                return render_template("main_page.html", texto = session["user"])

            return render_template("get_information.html")
        
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

        #Goes to function which checks if username and password were put right
        
        texto_register = new_user_check(request.form["runame"],request.form["rupass"])

        if texto_register == 1:

            db.session.execute(text(f'''INSERT INTO users (uname, upass) VALUES ('{request.form["runame"]}', '{generate_password_hash(request.form["rupass"])}')'''))
            db.session.commit()

            user = request.form["runame"]
            session["user"] = user

            return render_template("get_information.html")


    return render_template("register_page.html", texto_register = texto_register)

@app.route("/main_page", methods = ["POST", "GET"])

def main_page():

    return render_template("main_page.html",texto = session["user"])



@app.route("/get_information", methods = ["POST", "GET"])
def get_information():

    texten = ""

    if request.method == "POST":

        #print(request.form["name"],request.form["lname"],request.form["birthday"],request.form["gender"])
        #print(type(request.form["name"]),type(request.form["lname"]),type(request.form["birthday"]),type(request.form["gender"]))

        chekced_info = new_users_information_check(request.form["name"],request.form["lname"],request.form["birthday"])

        if chekced_info != 1:
            texten = chekced_info
        else:

            db.session.execute(text(f'''INSERT INTO users_information (user_name, birthday, gender, first_name, last_name) VALUES ('{session["user"]}', '{request.form["birthday"]}','{request.form["gender"]}','{request.form["name"]}','{request.form["lname"]}')'''))
            db.session.commit()

            return render_template("main_page.html",texto = session["user"])

    return render_template("get_information.html", fail_reason = texten)
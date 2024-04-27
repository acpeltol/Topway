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

def new_user_check(uname, upass, upass2):

    # If user didn't put both passwords right then it will inform about it

    if upass != upass2:
        return "You didn't reapeat your password right"

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
            
            texto = "Username or password is wrong"
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

            texto = "Username or password is wrong"

            return render_template("base.html", texto = texto)

    return render_template("base.html", texto = texto)

# REGISRATION PAGE





@app.route("/register", methods = ["POST", "GET"])
def register():

    texto_register = ""

    # If user writes down the name and the password it will go next statement

    if request.method == "POST":

        #Goes to function which checks if username and password were put right
        
        texto_register = new_user_check(request.form["runame"],request.form["rupass"], request.form["rupass2"])

        if texto_register == 1:

            db.session.execute(text(f'''INSERT INTO users (uname, upass) VALUES ('{request.form["runame"]}', '{generate_password_hash(request.form["rupass"])}')'''))
            db.session.commit()

            user = request.form["runame"]
            session["user"] = user

            return render_template("get_information.html")


    return render_template("register_page.html", texto_register = texto_register)






@app.route("/get_information", methods = ["POST", "GET"])
def get_information():

    texten = ""

    if request.method == "POST":

        chekced_info = new_users_information_check(request.form["name"],request.form["lname"],request.form["birthday"])

        if chekced_info != 1:
            texten = chekced_info
        else:

            db.session.execute(text(f'''INSERT INTO users_information (user_name, birthday, gender, first_name, last_name) VALUES ('{session["user"]}', '{request.form["birthday"]}','{request.form["gender"]}','{request.form["name"]}','{request.form["lname"]}')'''))
            db.session.commit()

            return render_template("main_page.html",texto = session["user"])

    return render_template("get_information.html", fail_reason = texten)

@app.route("/main_page", methods = ["POST", "GET"])






def main_page():
    return render_template("main_page.html", texto = session["user"])

# Friends page functions




@app.route("/friends", methods = ["POST", "GET"])
def friends():

        friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}' AND visible = True''')).fetchall()
        
        request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}' AND visible = True''')).fetchall()

        #request_list = ["fs","sf","th", "kaet"]

        return render_template("friends.html", len = len(friend_list), friend_list= friend_list, len_request = len(request_list), request_list = request_list)





@app.route("/friends_delete", methods = ["POST", "GET"])
def friends_delete():

    friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}'  AND visible = True''')).fetchall()
    

    for i in range(len(friend_list)):

        try:

            #print(request_list[i][0])
            kate = request.form[friend_list[i][0]]

            db.session.execute(text(f'''UPDATE friends SET visible=FALSE WHERE user_name = '{session["user"]}' AND friend_name = '{friend_list[i][0]}' '''))

            db.session.execute(text(f'''UPDATE friends SET visible=FALSE WHERE friend_name = '{session["user"]}' AND user_name = '{friend_list[i][0]}' '''))
            
            db.session.commit()

            break
        except:


            pass


    return friends()





@app.route("/friends_find", methods = ["POST"])
def friends_find():
        
        
        friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}' AND visible = True''')).fetchall()
        
        request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}' AND visible = True''')).fetchall()

        #request_list = ["fs","sf","th", "kaet"]

        found_friend = db.session.execute(text(f'''SELECT uname FROM users
                                   WHERE uname = '{request.form["find_name"]}' ''')).fetchall()
        
        if len(found_friend) != 1:

            return render_template("friends.html", len = len(friend_list), friend_list= friend_list, len_request = len(request_list), request_list = request_list, user_not_found = "This user doesn't exist")
        
        else:

            return render_template("friends_get.html", len = len(friend_list), friend_list= friend_list, len_request = len(request_list), request_list = request_list, found_friend = found_friend)





@app.route("/friend_request", methods = ["POST"])
def friend_request():

    check = db.session.execute(text(f'''SELECT * FROM friend_request
                                   WHERE from_name = '{session["user"]}' AND to_name = '{request.form["friend_request_info"]}' AND visible = True''')).fetchall()
    
    check2 = db.session.execute(text(f'''SELECT * FROM friends
                                   WHERE user_name = '{session["user"]}' AND friend_name = '{request.form["friend_request_info"]}' AND visible = True''')).fetchall()

    if len(check) == 0 and len(check2) == 0 and session["user"] != request.form["friend_request_info"]:


        check3 = db.session.execute(text(f'''SELECT * FROM friend_request
                                   WHERE from_name = '{session["user"]}' AND to_name = '{request.form["friend_request_info"]}' AND visible = FALSE''')).fetchall()
        
        if len(check3) == 0:

            db.session.execute(text(f'''INSERT INTO friend_request (from_name, to_name) VALUES ('{session["user"]}', '{request.form["friend_request_info"]}')'''))
            db.session.commit()

        else:
            db.session.execute(text(f'''UPDATE friend_request SET visible=True WHERE to_name = '{request.form["friend_request_info"]}' AND from_name = '{session["user"]}' '''))
            db.session.commit()


    return friends()




@app.route("/friend_request_accept", methods = ["POST"])
def friend_request_accept():
    
    request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}'  AND visible = True''')).fetchall()
    

    for i in range(len(request_list)):

        print(request_list[i][0])
        try:

            #print(request_list[i][0])
            kate = request.form[request_list[i][0]]

            db.session.execute(text(f'''UPDATE friend_request SET visible=FALSE WHERE to_name = '{session["user"]}' AND from_name = '{request_list[i][0]}' '''))

            check = db.session.execute(text(f'''SELECT * FROM friends
                                   WHERE user_name = '{session["user"]}' AND friend_name = '{request_list[i][0]}' AND visible = FALSE''')).fetchall()

            if len(check) == 0:

                db.session.execute(text(f'''INSERT INTO friends (user_name, friend_name) VALUES ('{session["user"]}', '{request_list[i][0]}')'''))

                db.session.execute(text(f'''INSERT INTO friends (user_name, friend_name) VALUES ('{request_list[i][0]}', '{session["user"]}')'''))

            else:

                db.session.execute(text(f'''UPDATE friends SET visible=True WHERE user_name = '{session["user"]}' AND friend_name = '{request_list[i][0]}' '''))

                db.session.execute(text(f'''UPDATE friends SET visible=True WHERE friend_name = '{session["user"]}' AND user_name = '{request_list[i][0]}' '''))
            
            db.session.commit()

            break
        except:
            pass


    return friends()





@app.route("/friend_request_decline", methods = ["POST"])
def friend_request_decline():
    
    request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}' AND visible = True''')).fetchall()
    

    for i in range(len(request_list)):

        print(request_list[i][0])
        try:

            print(type(request.form[request_list[i][0] + "_pita"]))

            print(request_list[i][0])
            #kate = request.form[request_list[i][0]]

            db.session.execute(text(f'''UPDATE friend_request SET visible=FALSE WHERE to_name = '{session["user"]}' AND from_name = '{request_list[i][0]}' '''))
            db.session.commit()

            break

        except:

            print("nope")

            pass


    return friends()

# Profile pages

@app.route("/profile", methods = ["POST", "GET"])
def profile():
    return render_template("profile.html")



#Message pages

@app.route("/messages", methods = ["POST", "GET"])
def messages():
    return render_template("messages.html", len_recived = 0, len_sent = 0)


@app.route("/send_message", methods = ["POST", "GET"])
def send_message():
    return render_template("send_message.html")

@app.route("/send_check", methods = ["POST", "GET"])
def send_check():
    
    to = request.form["to_user"]

    mes = request.form["messag"]

    date = datetime.datetime.now()

    date = str(date)

    check = db.session.execute(text(f'''SELECT * FROM users
                                   WHERE uname = '{to}' ''')).fetchall()
    
    if len(check) == 0:
        return render_template("send_message.html", wrong_user = "This user doesn't exist")

    db.session.execute(text(f'''INSERT INTO messages (from_name, message, to_user, datetime)
                                   VALUES ('{session["user"]}', '{mes}','{to}','{date}') '''))
    db.session.commit()


    return messages()
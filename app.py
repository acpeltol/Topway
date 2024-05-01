from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from os import getenv
import secrets

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)


#Routes to different pages



#####################


#Opening page


#######################


# Log in page


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

            session["csrf_token"] = secrets.token_hex(16)



            u_id = db.session.execute(text(f'''  
                    SELECT * FROM users_information WHERE user_name = '{session["user"]}' ''')).fetchall()
            
            if len(u_id) == 1:
                return render_template("main_page.html", texto = session["user"])

            return render_template("get_information.html")
        
        else:

            texto = "Username or password is wrong"

            return render_template("base.html", texto = texto)

    return render_template("base.html", texto = texto)



########################################





# REGISRATION PAGE




#####################




# Checks if new users username exists and if it has correct type password

def new_user_check(uname, upass, upass2):

    # If user didn't put both passwords right then it will inform about it

    if upass != upass2:
        return "You didn't reapeat your password right"

    # If user types nothing then it rejects sign up
    
    if uname == "" or upass == "":
        return "Wrog type of name or password"
    
    # If username alredy exists it rejects username

    u_id = db.session.execute(text(f'''SELECT id FROM users WHERE uname = '{uname}' ''')).fetchall()

    if len(u_id) == 1:        
        return "Username alredy exists"

    return 1


# Function which leads to registration page


@app.route("/register", methods = ["POST", "GET"])
def register():

    texto_register = ""

    # If user writes down the name and the password it will go next statement

    if request.method == "POST":

        #Goes to function which checks if username and password were put right
        
        texto_register = new_user_check(request.form["runame"],request.form["rupass"], request.form["rupass2"])

        if texto_register == 1:

            db.session.execute(text(f'''INSERT INTO users (uname, upass) VALUES 
                                    ('{request.form["runame"]}', '{generate_password_hash(request.form["rupass"])}')'''))
            db.session.commit()

            user = request.form["runame"]
            session["user"] = user

            return render_template("get_information.html")


    return render_template("register_page.html", texto_register = texto_register)




################################





# Get information page






################################




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


# Functions which leads to get_information page


@app.route("/get_information", methods = ["POST", "GET"])
def get_information():

    texten = ""

    if request.method == "POST":

        chekced_info = new_users_information_check(request.form["name"],request.form["lname"],request.form["birthday"])

        if chekced_info != 1:
            texten = chekced_info
        else:

            db.session.execute(text(f'''INSERT INTO users_information (user_name, birthday, gender, first_name, last_name) 
                                    VALUES ('{session["user"]}', '{request.form["birthday"]}','{request.form["gender"]}','{request.form["name"]}','{request.form["lname"]}')'''))
            db.session.commit()

            return render_template("main_page.html",texto = session["user"])

    return render_template("get_information.html", fail_reason = texten)

@app.route("/main_page", methods = ["POST", "GET"])

###########################



# Main page



#########################


# function which leads to main page

def main_page():
    return render_template("main_page.html", texto = session["user"])


########################



# Friends page functions


########################


# Function to friends page

@app.route("/friends", methods = ["POST", "GET"])
def friends():

        friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}' AND visible = True''')).fetchall()
        
        request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}' AND visible = True''')).fetchall()

        return render_template("friends.html", len = len(friend_list), friend_list = friend_list, len_request = len(request_list), request_list = request_list)


# Function which deletes a friend


@app.route("/friends_delete", methods = ["POST", "GET"])
def friends_delete():

    friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}'  AND visible = True''')).fetchall()
    

    for i in range(len(friend_list)):

        try:

            #print(request_list[i][0])
            kate = request.form[friend_list[i][0]]

            if session["csrf_token"] != request.form[friend_list[i][0]+"_c_delete"]:
                abort(403)

            db.session.execute(text(f'''UPDATE friends SET visible=FALSE WHERE user_name = 
                                    '{session["user"]}' AND friend_name = '{friend_list[i][0]}' '''))

            db.session.execute(text(f'''UPDATE friends SET visible=FALSE WHERE friend_name =
                                     '{session["user"]}' AND user_name = '{friend_list[i][0]}' '''))
            
            db.session.commit()

            break
        except:


            pass


    return friends()


# Page which shows searched user and fiend request button


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


# Function which sends friend request


@app.route("/friend_request", methods = ["POST"])
def friend_request():

    if session["csrf_token"] != request.form["friend_request_c"]:
        abort(403)
        #print("hey")

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


# Function which accepts othe user's friend request


@app.route("/friend_request_accept", methods = ["POST"])
def friend_request_accept():
    
    request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}'  AND visible = True''')).fetchall()
    

    for i in range(len(request_list)):

        try:

            kate = request.form[request_list[i][0]]

            if session["csrf_token"] != request.form[request_list[i][0]+"_c_accept"]:
                abort(403)



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


# Function which declines othe user's friend request


@app.route("/friend_request_decline", methods = ["POST"])
def friend_request_decline():
    
    request_list = db.session.execute(text(f'''SELECT from_name FROM friend_request
                                   WHERE to_name = '{session["user"]}' AND visible = True''')).fetchall()
    

    for i in range(len(request_list)):

        try:

            type = request.form[request_list[i][0] + "_pita"]

            if session["csrf_token"] != request.form[request_list[i][0]+"_c_decline"]:
                abort(403)


            db.session.execute(text(f'''UPDATE friend_request SET visible=FALSE WHERE to_name = '{session["user"]}' AND from_name = '{request_list[i][0]}' '''))
            db.session.commit()

            break

        except:

            pass


    return friends()


###########################




# Profile pages



###################



#Page for profile



@app.route("/profile", methods = ["POST", "GET"])
def profile():

    user = db.session.execute(text(f'''SELECT * FROM users_information
                                        WHERE user_name = '{session["user"]}' ''')).fetchall()

    return render_template("profile.html", user = user[0][0], first_name = user[0][3], last_name = user[0][4], Birtday = user[0][1], Sex = user[0][2])


# Function that show orfile of a friend


@app.route("/friend_profile", methods = ["POST", "GET"])
def friend_profile():

    fito = None

    friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}'  AND visible = True''')).fetchall()
    

    for i in range(len(friend_list)):

        try:

            kate = request.form[friend_list[i][0]+"_profile"]

            fito = friend_list[i][0]

            
            break
        except:
            pass

    user = db.session.execute(text(f'''SELECT * FROM users_information
                                   WHERE user_name = '{fito}' ''')).fetchall()

    return render_template("profile.html", user = user[0][0], first_name = user[0][3], last_name = user[0][4], Birtday = user[0][1], Sex = user[0][2])



####################





#Message pages



#####################


# Main message paig

@app.route("/messages", methods = ["POST", "GET"])
def messages():

    recived_list = db.session.execute(text(f'''SELECT * FROM messages
                                   WHERE to_user = '{session["user"]}' ORDER BY id DESC''')).fetchall()

    return render_template("messages.html", len_recived = len(recived_list), recived_list = recived_list)


# Page for sending messages


@app.route("/send_message", methods = ["POST", "GET"])
def send_message():


    friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}' AND visible = True''')).fetchall()

    #csrf = session["csrf_token"]

    return render_template("send_message.html", len = len(friend_list), friend_list = friend_list)


# Function to check user's message


@app.route("/send_check", methods = ["POST", "GET"])
def send_check():


    if session["csrf_token"] != request.form["message_c"]:
        abort(403)


    
    to = request.form["to_user"]

    mes = request.form["messag"]

    date = datetime.datetime.now()

    date = str(date)

    check = db.session.execute(text(f'''SELECT * FROM users
                                   WHERE uname = '{to}' ''')).fetchall()
    
    if len(check) == 0:

        friend_list = db.session.execute(text(f'''SELECT friend_name FROM friends
                                   WHERE user_name = '{session["user"]}' AND visible = True''')).fetchall()

        return render_template("send_message.html", wrong_user = "This user doesn't exist", len = len(friend_list), friend_list = friend_list)

    db.session.execute(text(f'''INSERT INTO messages (from_name, message, to_user, datetime)
                                   VALUES ('{session["user"]}', '{mes}','{to}','{date}') '''))
    db.session.commit()


    return messages()




#Page to see all messages that were sent




@app.route("/sent_messages", methods = ["POST", "GET"])
def sent_messages():
    
    sent_list = db.session.execute(text(f'''SELECT * FROM messages
                                   WHERE from_name = '{session["user"]}' ORDER BY id DESC''')).fetchall()

    return render_template("sent_messages.html", len_sent = len(sent_list), sent_list = sent_list)

##############






# Logout





###############


# Logout page

@app.route("/logout")
def logout():
    del session["user"]
    return index()
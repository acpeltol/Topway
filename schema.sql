




CREATE TABLE users (id SERIAL PRIMARY KEY, 
                uname TEXT, 
                upass TEXT);


CREATE TABLE users_information (user_name TEXT, 
                birthday DATE, 
                gender TEXT, 
                first_name TEXT, 
                last_name TEXT);

CREATE TABLE friends (user_name TEXT, 
                friend_name TEXT, 
                visible BOOLEAN);


CREATE TABLE friend_request (from_name TEXT, 
            to_name TEXT, 
            visible BOOLEAN);


CREATE TABLE messages (id SERIAL PRIMARY KEY, 
                    from_name TEXT, 
                    message TEXT, 
                    to_user TEXT, 
                    datetime TEXT);

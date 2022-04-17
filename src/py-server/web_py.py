'''
Created April 16th, 2022
@author: Kenenna N. Okeke (https://kenenna.com)
@note: Python Auth Microservice Example - Server
'''

# Importations
from flask import Flask
from flask_restful import Resource, Api, reqparse
import jwt
import MySQLdb
import time
import bcrypt

app = Flask(__name__)
api = Api(app)

# Fetch these from your environment
secret = "S6eubevKOSxsyOEL5zE3xAVDdsznOFYG" # JWT encryption key
db_host = '127.0.0.1' # MySQL database host
db_name = 'todoist_primo' # MySQL database name
db_usr = 'root' # MySQL database username
db_pwd = 'password' # MySQL database password

class Login(Resource):
    def post(self): # A post to /login has occured
        
        # Make email and password arguments required
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        
        # Establish our connection to the database
        db = MySQLdb.connect(host=db_host, database=db_name, user=db_usr, password=db_pwd)
        
        email = db.escape_string(args['email']).decode("utf-8")
        password = (args['password']).encode("utf-8")
        
        q = db.cursor()
        # Select whatever information you'd like to pass in the JWT (or send elsewhere) here and map it below
        q.execute('SELECT `first_name`, `last_name`, `email`, `password`, `id` FROM `users` WHERE `email`="' + email + '"')
        r = q.fetchone()
        if(r is not None):
            user_password = r[3]
            user_fname = r[0]
            user_lname = r[1]
            user_email = r[2]
            user_id = r[4]
            
            # Compare the passwords
            if(bcrypt.checkpw(password, user_password.encode("utf-8"))):
                token = jwt.encode({"id": user_id, "created_at": time.time()}, secret, algorithm="HS256") # Timestamp will be our random variable.
                payload = {"success": True, "email": user_email, "token": token}
            else:
                payload = {"success": False, "error" : "Invalid Password"}
        else:
            payload = {"success": False, "error": "User Not Found"}
        return payload

# Create HTTP Endpoint for logins
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(port="8000", debug=True)

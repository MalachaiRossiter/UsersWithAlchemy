from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import recipe
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DB = "recipes_schema"

class User:
    def __init__(self,user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.email = user['email']
        self.password = user['password']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']

    #Start here to create new User. --- Step 1
    @classmethod
    def create_user(cls, user):

        if not cls.validate_user(user):
            return False

        parsed_data = {
            'first_name' : user['first_name'],
            'last_name' : user['last_name'],
            'email' : user['email'].lower(), 
            'password' : bcrypt.generate_password_hash(user['password'])
        }
        print("parsed_data", parsed_data)
        query = "INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        new_user = connectToMySQL(DB).query_db(query,parsed_data)
        user_id = cls.get_id(new_user)
        print('user_id', user_id)
        return user_id

    @classmethod
    def get_id(cls, user_id):

        data = {'id': user_id}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result [0])

    #Checks if the email is in the database already. ---Step 3 in Authenticating the New User, Go back to finish step 2
    @classmethod
    def get_email(cls,email):
        data = {"email": email.lower()}

        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])


    #checking if the username has been filled out propperly ---Step 2 in Authentication
    @classmethod
    def validate_user(cls, user):
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash('First name needs to be longer', 'registration')
        if len(user['last_name']) < 3:
            is_valid = False
            flash('Last Name needs to be longer', 'registration')
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash('this aint no email chump', 'registration')
        if not user['password'] == user['confirm_password']:
            flash('yo you cant type very well can you', 'registration')
            is_valid = False
        #checking for an existing email
        used_email = User.get_email(user['email'])
        if used_email:
            flash("An account already has that email nerd", 'registration')
            is_valid=False

        return is_valid

    #Login method
    @classmethod
    def authenticate_user(cls, user):

        existing_user = cls.get_email(user["email"])
        if not existing_user:
            flash('this email doesnt exist chump', 'login')
            return existing_user

        if not bcrypt.check_password_hash(existing_user.password, user['password']):
            return False
        
        return existing_user
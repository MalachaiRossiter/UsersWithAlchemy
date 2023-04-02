from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models.address import Address
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DB = "test_schema"

class User: 
    def __init__(self,user):
        self.id = user['id']
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.age = user['age']
        self.email = user['email']
        self.password = user['password']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']
        self.address_id = user['address_id']

    def to_dict(self):
        address_ids = [self.address_id]
        addresses = Address.get_all_for_ids(address_ids)
        address = addresses[0] if addresses else None

        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'password': self.password,
            'address_id': self.address_id,
            'address': address.to_dict() if address else None
        }

    #create new user
    @classmethod
    def create_user(cls, user):

        if not cls.validate_user(user):
            return False
        
        parsed_data = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'age': user['age'],
            'email': user['email'],
            'password': bcrypt.generate_password_hash(user['password']),
            'address_id': user['address_id']
        }
        query = 'INSERT INTO users (first_name, last_name, age, email, password, address_id) VALUES (%(first_name)s, %(last_name)s, %(age)s, %(email)s, %(password)s, %(address_id)s);'
        new_user = connectToMySQL(DB).query_db(query,parsed_data)
        user_id = cls.get_id(new_user)
        print('user_id:', user_id)
        return user_id
    
    #update user
    @classmethod
    def update_user(cls, user, user_id):
        if not cls.validate_user(user):
            return False
        data = {
            'id': user_id,
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'age': user['age'],
            'email': user['email'],
            'address_id': user['address_id']
        }
        query = 'UPDATE test_schema.users SET first_name = %(first_name)s, last_name = %(last_name)s, age = %(age)s, email = %(email)s, address_id = %(address_id)s WHERE id = %(id)s'
        connectToMySQL(DB).query_db(query, data)
        result = User.get_id(user_id)
        return (result)
    
    #delete user
    @classmethod
    def delete_user(cls, user_id):
        data = {
            'id' : user_id
        }
        query = 'DELETE FROM users WHERE id = %(id)s'
        connectToMySQL(DB).query_db(query, data)
        return {'msg': f'deleted user at id: {user_id}'}


    #get user by id
    @classmethod
    def get_id(cls, user_id):

        data = {'id': user_id}
        query = 'SELECT * FROM users LEFT JOIN addresses ON users.address_id = addresses.id WHERE users.id = %(id)s;'
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])
    
    #get all users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM test_schema.users LEFT JOIN addresses ON users.address_id = addresses.id;"
        result = connectToMySQL(DB).query_db(query)
        return [cls(user) for user in result]
    
    #gets email
    @classmethod
    def get_email(cls,email):
        data = {"email": email.lower()}

        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    #validate new user
    @classmethod
    def validate_user(cls, user):
        is_valid = True
        if len(user['first_name']) < 2:
            is_valid = False
            flash('User Name needs to be longer')
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash('this aint no email chump', 'registration')
        return is_valid
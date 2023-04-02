from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.address import Address

DB = "test_schema"

class User: 
    def __init__(self,user):
        self.id = user['id']
        self.name = user['name']
        self.created_at = user['created_at']
        self.updated_at = user['updated_at']
        self.address_id = user['address_id']

    def to_dict(self):
        address_ids = [self.address_id]
        addresses = Address.get_all_for_ids(address_ids)
        address = addresses[0] if addresses else None

        return{
            'name': self.name,
            'address_id': self.address_id,
            'address': address.to_dict() if address else None
        }

    #create new user
    @classmethod
    def create_user(cls, user):

        if not cls.validate_user(user):
            return False
        
        parsed_data = {
            'name' : user['name'],
            'address_id' : user['address_id']
        }
        query = 'INSERT INTO users (name, address_id) VALUES (%(name)s, %(address_id)s);'
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
            'name': user['name'],
            'address_id': user['address_id']
        }
        query = 'UPDATE test_schema.users SET name = %(name)s, address_id = %(address_id)s WHERE id = %(id)s'
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
    
    #validate new user
    @classmethod
    def validate_user(cls, user):
        is_valid = True
        if len(user['name']) < 2:
            is_valid = False
            flash('User Name needs to be longer')
        return is_valid
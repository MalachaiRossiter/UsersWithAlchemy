from ast import Delete
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

bcrypt = Bcrypt(app)

DB = "recipes_schema"

class Recipe:
    def __init__(self, recipe):
        self.id = recipe['id']
        self.name = recipe['name']
        self.description = recipe['description']
        self.instruction = recipe['instruction']
        self.time = recipe['time30']
        self.date = recipe['date']
        self.created_at = recipe["created_at"]
        self.updated_at = recipe["updated_at"]
        self.user = None

    @classmethod
    def create_recipe(cls, recipe):

        if not cls.validate_recipe(recipe):
            return False
        
        data = {
            'name': recipe['name'],
            'description': recipe['description'],
            'instruction': recipe['instruction'],
            'time30': recipe['time30'],
            'date': recipe['date'],
            'users_id': session['user_id']
        }
        print("data is cool", data)
        query = "INSERT into recipes (name, description, instruction, time30, date, users_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(time30)s, %(date)s, %(users_id)s);"
        new_recipe = connectToMySQL(DB).query_db(query,data)
        print(new_recipe)
        return True

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.users_id;"
        result = connectToMySQL(DB).query_db(query)
        print('result of query', result)
        return result

    @classmethod
    def get_recipe(cls,recipe_id):
        data = {'id': recipe_id}
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        recipe = connectToMySQL(DB).query_db(query,data)
        print("The Database has this for the Recipe: ", recipe)
        return cls(recipe[0])

    @classmethod
    def update_recipe(cls, recipe,recipe_id):

        if not cls.validate_recipe(recipe):
            return False
        data = {
            'name': recipe['name'],
            'description': recipe['description'],
            'instruction': recipe['instruction'],
            'time30': recipe['time30'],
            'date': recipe['date'],
            'id': recipe_id
        }
        query = "UPDATE recipes_schema.recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, time30 = %(time30)s, date = %(date)s WHERE id = %(recipe_id)s"
        result = connectToMySQL(DB).query_db(query)
        print("result of the update", result)
        return result



    @classmethod
    def delete_recipe(cls,recipe_id):
        data = {'id': recipe_id}
        query = "DELETE FROM recipes WHERE id = %(id)s"
        connectToMySQL(DB).query_db(query,data)

    @classmethod
    def validate_recipe(cls, recipe):
        is_valid=True
        if len(recipe['name']) < 1:
            flash('there isnt enough information')
            is_valid=False
            return is_valid
        if len(recipe['description']) < 1:
            flash('there isnt enough information')
            is_valid=False
            return is_valid
        if len(recipe['instruction']) < 1:
            flash('there isnt enough information')
            is_valid=False
            return is_valid
        return is_valid
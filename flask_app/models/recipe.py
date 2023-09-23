from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import user

class Recipe:
    DB = 'recipes_db_flask'
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.under_30 = data["under_30"]
        self.instructions = data["instructions"]
        self.date = data['date']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None




# validate methods

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data["name"]) <= 0 or len(data["description"]) <= 0 or len(data["instructions"]) <= 0 :
            is_valid = False
            flash("All fields required")
            return is_valid
        if len(data['name']) < 2:
            flash("Recipe must be at least 2 characters")
            is_valid = False
        if len(data['description']) < 2:
            flash("Description must be at least 2 characters")
            is_valid = False
        if len(data['instructions']) < 2:
            flash("Instructions must be at least 2 characters")
            is_valid = False
        if len(data['date']) < 1:
            flash("Please enter a date cooked date.")
            is_valid = False
        if (data['under_30'] != 'yes' and data['under_30'] != 'no'):
            flash("Under 30 must be either yes or no!")
            is_valid = False
        

        return is_valid
    


# others Methods

    # CREATE NEW RECIPE
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, under_30, instructions, date, created_at,  user_id) VALUES (%(name)s, %(description)s, %(under_30)s, %(instructions)s,  %(date)s, NOW(), %(user_id)s)"
        results = connectToMySQL(cls.DB).query_db(query,data)
        recipe_id_created = results  # 
        return recipe_id_created # Create returns the ID of the new recipe
    
    

    # # READ
    # # ONE elt
    @classmethod
    def get_recipe_with_user(cls, data):

        query = """SELECT * FROM recipes 
                   LEFT JOIN users ON recipes.user_id = users.id 
                   WHERE recipes.id = %(recipe_id)s;"""

        results = connectToMySQL(cls.DB).query_db(query, data)

        recipe_instance = Recipe(results[0])

        for obj in results:

            user_data = {
                "id" : obj["users.id"],
                "first_name" : obj["first_name"],
                "last_name" : obj["last_name"],
                "email" : obj["email"],
                "password" : obj["password"],
                "created_at" : obj["users.created_at"],
                "updated_at" : obj["users.updated_at"],
            }
            user_instance = user.User(user_data)
            recipe_instance.user = user_instance

        return recipe_instance



    # # READ
    # # ONE elt
    @classmethod
    def get_one(cls, data):
        query  = "SELECT * FROM recipes WHERE id = %(recipe_id)s;"

        results = connectToMySQL(cls.DB).query_db(query, data)

        return cls(results[0])
    


    # UPDATE
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_30 = %(under_30)s, instructions = %(instructions)s, date = %(date)s, updated_at = NOW() WHERE id = %(recipe_id)s"

        results = connectToMySQL(cls.DB).query_db(query, data)

        return  # update queries don't return anything 



    # DELETE     
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s"

        results = connectToMySQL(cls.DB).query_db(query, data)

        return  # delete queries don't return anything



    # GET ALL RECIPES
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)

        all_recipes = []

        for obj in results:
            recipe_instance = Recipe(obj)

            user_data = {
                "id" : obj["users.id"],
                "first_name" : obj["first_name"],
                "last_name" : obj["last_name"],
                "email" : obj["email"],
                "password" : obj["password"],
                "created_at" : obj["users.created_at"],
                "updated_at" : obj["users.updated_at"],
            }
             
            user_instance = user.User(user_data)

            recipe_instance.user = user_instance

            all_recipes.append(recipe_instance)

        return all_recipes



   







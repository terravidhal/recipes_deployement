from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
import re




class User:
    DB = 'recipes_db-new'
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]




# validate Methods

    # VALIDATE USER INFOS (REGISTER FORM)
    @staticmethod
    def validate_user_infos(data):
        PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') 
        #requires 8 chars, 1 upper, 1 lower, 1 number
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data["fname"]) <= 0 or len(data["lname"]) <= 0 or len(data["eml"]) <= 0 or len(data["psswrd"]) <= 0:
            is_valid = False
            flash("All fields required", "register")
            return is_valid
        if len(data["fname"]) < 2:
            is_valid = False
            flash("First Name must be at least 2 characters", "register")
        if len(data["lname"]) < 2:
            is_valid = False
            flash("Last Name must be at least 2 characters", "register")
        if not EMAIL_REGEX.match(data['eml']):
            flash("Invalid email address")
            is_valid = False
        if not PASSWORD_REGEX.match(data['psswrd']):
            flash("requires 8 chars, 1 upper or lower, 1 number", "register")
            is_valid = False    
        if data["psswrd"] != data["conf_pass"]:
            flash("Passwords don't match....you gotta fix that.", "register")    
            is_valid = False    

        return is_valid


    # VALIDATE USER INFOS (LOGIN FORM)
    @classmethod
    def user_with_specific_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:  
            return False
        return cls(result[0])



# others Methods
    
    # CREATE NEW USER
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(fname)s, %(lname)s, %(eml)s, %(psswrd)s, NOW())"

        results = connectToMySQL(cls.DB).query_db(query,data)
        
        user_id_created = results
        return user_id_created 
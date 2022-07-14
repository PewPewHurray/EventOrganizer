from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "eome_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.coordinating = []
        self.participating = []

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return False
        return cls(results[0])

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE is = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        return user

    @staticmethod
    def validate_registration(data):
        is_valid = True
        valid_password = True
        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters long", "registration")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters long", "registration")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Not a valid email address", "registration")
            is_valid = False
        else:
            user = User.get_by_email(data)
            if user != False:
                if data["email"] == user.email:
                    flash("That email has already been used", "registration")
                    is_valid = False
        weak_passwords = ['LetMeIn1!', "Password123!", "Opensesame1!"]
        if data["password"] in weak_passwords:
            flash("Please pick a stronger password", "registration")
            valid_password = False
        if len(data["password"]) < 8:
            flash("Password is too short", "registration")
            valid_password = False
        if data["password"].isalnum():
            flash("Password is missing a special character", "registration")
            valid_password = False
        if data["password"].islower():
            flash("Password is missing a uppercase letter", "registration")
            valid_password = False
        if data["password"].isupper():
            flash("Password is missing a lowercase letter", "registration")
            valid_password = False
        num_test = False
        letter_test = False
        for x in data["password"]:
            if x.isdigit():
                num_test = True
                if letter_test:
                    break
            elif x.isalnum():
                letter_test = True
        if not letter_test:
            flash("Password needs a uppercase and lowercase letter", "registration")
            valid_password = False
        if not num_test:
            flash("Password is missing a number", "registration")
            valid_password = False
        if valid_password:
            if data["password"] != request.form["confirm_password"]:
                flash("Passwords do not match", "registration")
                is_valid = False
        else:
            is_valid = False
        return is_valid
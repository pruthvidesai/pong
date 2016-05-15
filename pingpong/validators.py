from re import search
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Validator:
    def __init__(self):
        self.valid = False

    def username(self, username):
        user = User.objects.filter(username=username)
        if user:
            return ValidationError("Username exists, please use a different username")
        elif not search(r'^\w+$', username):
            return ValidationError("Username only accepts alphanumeric characters and underscore")

    def email(self, email):
        if not email.endswith("@hds.com"):
            return ValidationError("Please enter your HDS email")

    def password(self, password, confirm_password):
        if password is not confirm_password:
            return ValidationError("Passwords don't match")
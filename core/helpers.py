from typing import Dict, Tuple
from django.contrib.auth.models import User


class UserHelper:
    def __init__(self, first_name, last_name, username, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def validate(self) -> Tuple[bool, Dict]:
        errors = {}

        if not self.first_name:
            errors['error_first_name'] = 'First name is required'

        if not self.last_name:
            errors['error_last_name'] = 'Last name is required'

        if not self.username:
            errors['error_username'] = 'Username is required'

        if not self.password:
            errors['error_password'] = 'Password is required'

        # Check if user with this username already exists
        if User.objects.filter(username=self.username).first():
            errors['error_username'] = 'User with this username already exists'

        return not bool(len(errors.keys())), errors


    def save(self) -> User:
        user = User(first_name=self.first_name, last_name=self.last_name, username=self.username)
        user.set_password(self.password)
        return user.save()

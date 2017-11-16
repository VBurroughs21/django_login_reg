from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def login(self, email, password):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = []

        if not(email_regex.match(email)):
            errors.append('Valid email required')
            return {'errors': errors}
        else:
            return {'user': {
                'first_name': 'Nope'
            }}


    def register(self, info):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        name_regex = re.compile(r'^[a-zA-Z]')
        errors = []

        # Validations
        if not('first_name' in info) or len(info['first_name']) < 2 or not(name_regex.match(info['first_name'])):
            errors.append('First name required; No fewer than 2 characters; letters only')

        if not('last_name' in info) or len(info['last_name']) < 2 or not(name_regex.match(info['last_name'])):
            errors.append('Last name required; No fewer than 2 characters; letters only')

        if not('email' in info) or not(email_regex.match(info['email'])):
            errors.append('Valid email required')

        if not('password' in info) or not('password_confirm' in info) or len(info['password']) < 8 or not(info['password'] == info['password_confirm']):
            errors.append('Password required; No fewer than 8 characters in length; Passwords must match')

        # Password encryption
        if len(errors) == 0:
            info['password'] = info['password'].encode()
            info['password'] = bcrypt.hashpw(info['password'], bcrypt.gensalt())

            User.objects.create(
                first_name = info['first_name'],
                last_name = info['last_name'],
                email = info['email'],
                password = info['password']
            )
            return {
                'new_user': info
            }
        else:
            return {
                'errors': errors
            }


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

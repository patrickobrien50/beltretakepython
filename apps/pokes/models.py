from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

Email_Regex = re.compile (r'^[a-zA-Z0-9.+_]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
Name_Regex = re.compile (r'^[a-zA-Z]+$')

class LoginManager(models.Manager):
    def validateRegister(self, postData):
        status = True
        errorlist = []
        if not Name_Regex.match(postData['name']):
            errorlist.append("Must provide valid name!")
            status = False
        if not Name_Regex.match(postData['alias']):
            errorlist.append("Must provide valid alias!")
            status = False
        if len(postData['name']) < 2 or len(postData['alias']) < 2:
            errorlist.append("Name and alias must have at least 2 letters!")
            status = False
        if not Email_Regex.match(postData['email']):
            errorlist.append("Must provide a valid email!")
            status = False
        if len(postData['password']) < 8:
            errorlist.append("Password must be at least 8 characters!")
            status = False
        if postData['password'] != postData['confirm']:
            errorlist.append("Passwords must match!")
            status = False
        if len(User.objects.filter(email=postData['email'])) > 0:
            errorlist.append("Email is already registered!")
            status = False
        if status == False:
            return (False, errorlist)
        else:
            password = postData['password']
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            newuser = User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hashed, birthday=postData['birthday'])
            return (True, newuser)

    def loginValidate(self, postData):
        olduser = User.objects.filter(email=postData['email'])
        status = True
        errorlist = []
        if len(olduser) < 1:
            errorlist.append("Must register!")
            status = False
        if len(postData['email']) < 1:
            errorlist.append("Must provide a valid email!")
            status = False
        if len(postData['password']) < 1:
            errorlist.append("Must provide a valid password")
            status = False
        if status == False:
            return (False, errorlist)
        else:
            if bcrypt.hashpw(postData['password'].encode(), olduser[0].password.encode()) == olduser[0].password:
                return (True, olduser[0])
            else:
                errorlist.append("Incorrect Password")
                return (False, errorlist)


class User(models.Model):
    objects = LoginManager()
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    birthday = models.DateField()
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.IntegerField(default=0)

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="pokerpokes")
    poked = models.ForeignKey(User, related_name="pokedpokes")
    counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.

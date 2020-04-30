from django.db import models
import re

class LoginManager(models.Manager):
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must be longer than 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be longer than 2 characters"
        email = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email.match(post_data['email']):
            errors['email'] = 'Enter valid Email'
        result = User.objects.filter(email=post_data['email'])
        if len(post_data['password']) < 8:
            errors['password'] = "Password is too short!"
        if post_data['password'] != post_data['cPassword']:
            errors['cPassword'] = "Passwords do not match!"
        elif post_data['password'] != post_data['cPassword']:
            errors['cPassword'] = "Password Match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()

class Post(models.Model):
    user = models.ForeignKey(User, related_name="users_post", on_delete = models.CASCADE)
    post = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    posting = models.ForeignKey(Post, related_name="comment_on_post", on_delete = models.CASCADE)
    users_comments = models.ForeignKey(User, related_name="users_commenting_on_post", on_delete = models.CASCADE)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager 
from django.db import models 
class UserManager(BaseUserManager): 
    def create_user(self, email, password=None): 
     if not email: 
      raise ValueError("Users must have an email address") 
     email = self.normalize_email(email) 
     user = self.model(email=email) 
     user.set_password(password) 
     user.save(using=self._db) 
     return user 
 
    def create_superuser(self, email, password): 
        user = self.create_user(email, password) 
        user.is_admin = True 
        User.is_superuser = True 
        user.save(using=self._db) 
        return user 
 
class User(AbstractBaseUser): 
    email = models.EmailField(unique=True) 
    name = models.CharField(max_length =255) 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    images = models.FileField(upload_to='user_images/', null=True, blank=True)
    objects = UserManager() 
 
    USERNAME_FIELD = 'email'

class Recipie(models.Model):
        choice = (
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        )
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        title = models.CharField(max_length=255)
        ingredients = models.TextField()
        steps = models.TextField()
        cooking_time = models.IntegerField()
        difficulty_level = models.CharField(max_length=50,choices=choice)
        views = models.IntegerField(default=0)
        date = models.DateTimeField(auto_now_add=True)
        images = models.FileField(upload_to='recipie_images/', null=True, blank=True)

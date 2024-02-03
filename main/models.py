from lib2to3.pytree import Base
from operator import mod
from django.db import models
import uuid  # for generating uuid
import datetime

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager


# Create your models here.
# base model
class BaseModel(models.Model):
    """Base ORM model"""
    # create uuid field
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # created and updated at date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # meta class
    class Meta:
        abstract = True

    # Time elapsed since creation
    def get_seconds_since_creation(self):
        """
        Find how much time has been elapsed since creation, in seconds.
        This function is timezone agnostic, meaning this will work even if
        you have specified a timezone.
        """
        return (datetime.datetime.utcnow() -
                self.created_at.replace(tzinfo=None)).seconds


# User model table
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """A ORM model for Managing User and Authentication"""

    # mobile field
    mobile = models.BigIntegerField(unique=True,null =True)
    email =  models.EmailField(max_length = 254,unique=True,null = True,blank=True) 
    full_name = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    password = models.CharField(max_length=100)
    gender =models.CharField(max_length=100,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_serviceProvider = models.BooleanField(default=False)
    
    # create objs for management
    objects = UserManager()

    # SET email field as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # create a meta class
    class Meta:
        db_table= 'user'

class WorkingHours(BaseModel):
    day = models.CharField(max_length=100)
    start_hour = models.TimeField()
    end_hour = models.TimeField()


class ServiceProvider(BaseModel):
    working_from_date = models.DateField(null=False)
    rating = models.IntegerField()
    location = models.CharField(max_length=200)
    profession = models.CharField(max_length=100)
    working_hours = models.ForeignKey(WorkingHours,null=True,blank=True, on_delete=models.CASCADE)
    photo = models.CharField(max_length=200)
    user = models.ForeignKey(User,null=True,blank=True, on_delete=models.CASCADE)


class Category(BaseModel):
    name = models.CharField(max_length=100)


class SubCategory(BaseModel):
    category = models.ForeignKey(Category,null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)



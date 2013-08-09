from django.db import models
from django.contrib.auth.models import User
from time import time

def get_upload_file_name(instance, filename):
  return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)
 
# Create your models here.
class Food_type(models.Model):
 food_type_name = models.CharField(max_length=200)
 per_kg_emmision = models.DecimalField(max_digits=8, decimal_places=3)
 feedback = models.TextField()
 def __unicode__(self):
  return self.food_type_name
  
class feedback(models.Model):
 feedback = models.TextField()
 def __unicode__(self):
  return self.feedback
 
#class User(models.Model):
# display_name = models.CharField(max_length=100)
# name = models.CharField(max_length=100)
# def __unicode__(self):
#  return self.display_name


class Diary_entry(models.Model):   
 food_type = models.ForeignKey(Food_type)
 user = models.ForeignKey(User)
 entry_date = models.DateField()
 meal_type = models.CharField(max_length=100)
 serving_size = models.DecimalField(max_digits=6, decimal_places=3)
 additional_info = models.CharField(max_length=200)
 image = models.FileField( upload_to=get_upload_file_name)

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

 SIZE_CHOICES = (
    (0.05, '0.5'),
    (0.1, '100 Grams'),
    (0.15, '150 Grams'),
    (0.2, '200 Grams'),
    (0.25, '250 Grams'),
    (0.3, '300 Grams'),
    (0.35, '350 Grams'),
    (0.40, '400 Grams'),
    (0.45, '450 Grams'),
    (0.5, '500 Grams'),
    (0.55, '550 Grams'),
    (0.6, '600 Grams'),
    (0.65, '650 Grams'),
    (0.7, '700 Grams'),
    (0.75, '750 Grams'),
    (0.8, '800 Grams'),
    (0.85, '850 Grams'),
    (0.90, '900 Grams'),
    (0.95, '950 Grams'),
    (1, '1 Kilogram'),
    (1.5, '1.5 Kilograms'),
    (1.75, '1.75 Kilograms'),
    (2, '2 Kilograms'),)
    
 food_type = models.ForeignKey(Food_type)
 user = models.ForeignKey(User)
 entry_date = models.DateField()
 meal_type = models.CharField(max_length=100)
 serving_size = models.DecimalField(max_digits=6, decimal_places=3, choices=SIZE_CHOICES)
 additional_info = models.CharField(max_length=200)
 image = models.FileField( upload_to=get_upload_file_name)

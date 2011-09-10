from django.db import models

# Create your models here.

class ServiceRel(models.Model):
  name = models.CharField(max_length = 20)
  description = models.CharField(max_length = 1024, default='')

class ServiceCore(models.Model):
  latitude = models.IntegerField()
  longitude = models.IntegerField()
  name = models.CharField(max_length = 128,primary_key = True)
  type = models.CharField(max_length = 64)
  email = models.CharField(max_length = 64)
  phone = models.CharField(max_length = 32)
  description = models.CharField(max_length = 1024)
  address = models.CharField(max_length = 256)
  icon = models.CharField(max_length = 128)
  aveage = models.CharField(max_length = 5)
  days = models.CharField(max_length = 256)
  nation = models.CharField(max_length = 256, default = 'MIXED')
  pricelow = models.IntegerField(default = 20)
  pricehigh = models.IntegerField(default = 600)
  activate = models.BooleanField()
  grade = models.IntegerField(default = 0);
  activity = models.IntegerField(default  = 0);
  privilege = models.CharField(max_length = 32)
  extend = models.ForeignKey(ServiceRel)

class UserCore(models.Model):
  name = models.CharField(max_length = 64,unique = True)
  email = models.CharField(max_length = 64,primary_key = True)
  password = models.CharField(max_length = 64)

class History(models.Model):
  time = models.CharField(max_length = 32)
  type = models.CharField(max_length = 32)
  who = models.CharField(max_length = 64)
  service = models.CharField(max_length = 128)
  para = models.CharField(max_length = 1024)
  
#1mnjwdck@dolav_1iuy)-d^20$&b@c&_u7h_4$5slhfhz9k8jh

from django.db import models
from lxml import etree
from StringIO import StringIO
from main.core.models import Entity,EntityConfig
from main.core.user import *
from core import xmlbase

# Create your models here.

class Garden(models.Model):
  entity = models.ForeignKey(Entity)

# Associate a Garden with a fb_accout

def RegisterIconComponent(entity):
  data = """<icon name='icon' path='/res/error_res.png'/>"""
  xmlbase.CreateNewInfo(entity,data,'icon')

def  CreateGarden(user):
  entity = Entity()
  entity.name = user.username + "__garden"
  entity.email = user.email
  entity.description = "Zoyoe Garden Application"
  entity.category = "garden" 
  rel = EntityConfig.objects.get(name='default')
  entity.extend = rel
  entity.activate = True
  entity.save()
  garden = Garden()
  garden.entity = entity
  garden.save()
  RegisterIconComponent(garden.entity)
  InitEntityDir(garden.entity,None) 
  return garden

def GetGardenOption(user):
  try:
    garden = Garden.objects.get(entity__name = user.username + "__garden")
    return garden
  except Garden.DoesNotExist:
    return None
  
class Plant(models.Model):
  entity = models.ForeignKey(Entity)

def CreatePlant(pname):
  formal_name = GetFormalName(pname)
  if not formal_name:
    return None
  entity = Entity()
  entity.name = formal_name + "__plant"
  entity.email = "zoyoeproject@gmail.com"
  entity.description = "Zoyoe Plant"
  entity.category = "plant" 
  rel = EntityConfig.objects.get(name='plant')
  entity.extend = rel
  entity.activate = True
  entity.save()
  plant = Plant()
  plant.entity = entity
  plant.save()
  RegisterIconComponent(plant.entity)
  InitEntityDir(plant.entity,None) 
  return plant

def GetPlantOption(pname):
  try:
    plant = Plant.objects.get(entity__name = pname + "__plant")
    return plant 
  except Plant.DoesNotExist:
    return None
 

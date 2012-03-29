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
  data = """<icon name='tmpname' path='default/icon' size='default'>\
<description>Default Icon</description></icon>"""
  xmlbase.CreateNewInfo(entity,data,'icon')

def  CreateGarden(user):
  if (user.username.startswith('fb_')):
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
    InitEntityDir(garden.entity,None) 
    RegisterIconComponent(garden.entity)
    return garden
  else:
    return None

def GetGardenOption(user):
  try:
    garden = Garden.objects.get(entity__name = user.username + "__garden")
    return garden
  except Garden.DoesNotExist:
    return None
  


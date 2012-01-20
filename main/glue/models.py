from django.db import models
from lxml import etree
from StringIO import StringIO

from django.contrib.auth.models import User
from core.models import ServiceCore 

# Create your models here.

class CollectInfo(models.Model):
  time = models.DateField(auto_now_add = True)
  path = models.CharField(max_length = 128)
  user = models.ForeignKey(User)
  service = models.ForeignKey(ServiceCore)
    
def CreateCollectInfo(service,user):
  info = CollectInfo()
  info.user = user
  info.service = service
  info.path = "/"
  return info

def UsersOfService(serv):
  return CollectInfo.objects.filter(service = serv )

def ServicesOfUser(usr):
  return CollectInfo.objects.filter(user = usr)

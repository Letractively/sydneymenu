from django.db import models
from lxml import etree
from StringIO import StringIO

# Create your models here.

class Info(models.Model):
  time = models.DateField(auto_now_add = True)
  version = models.CharField(max_length = 64)
  path = models.CharField(max_length = 64)
  service = models.CharField(max_length = 128)
  data = models.CharField(max_length = 1024)

class ServiceConfig(models.Model):
  name = models.CharField(max_length = 128, unique = True)
  version = models.IntegerField()
  xslt = models.CharField(max_length = 4096, default='')
  xsd = models.CharField(max_length = 4096, default='')

  def GetXSDDoc(self):
    doc = etree.parse(StringIO(self.xsd))
    return doc

  def GetXSLT(self):
    xslt_doc = etree.parse(StringIO(self.xslt))
    return etree.XSLT(xslt_doc)


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
  days = models.CharField(max_length = 256)
  nation = models.CharField(max_length = 256, default = 'MIXED')
  pricelow = models.IntegerField(default = 20)
  pricehigh = models.IntegerField(default = 600)
  activate = models.BooleanField()
  grade = models.IntegerField(default = 0);
  activity = models.IntegerField(default  = 0);
  privilege = models.CharField(max_length = 32)
  extend = models.ForeignKey(ServiceConfig)

  def BuildComp(self):
    comp = {}
    db_items = Info.objects.filter(service = self.name)
    db_config = self.extend
    items = {}
    comp['ITEMS'] = items
    for item in db_items:
      if (not items.has_key(item.path)):
        items[item.path] = []
      comp[item.path].append(etree.parse(StringIO(item.data)))
    comp['CONFIG'] = db_config
    comp['RENDER'] = db_config.GetXSLT()
    return comp
  

class History(models.Model):
  time = models.DateField(auto_now_add = True)
  type = models.CharField(max_length = 32)
  who = models.CharField(max_length = 64)
  service = models.CharField(max_length = 128)
  para = models.CharField(max_length = 1024)



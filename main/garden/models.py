from django.db import models
from lxml import etree
from StringIO import StringIO

# Create your models here.

class Garden(models.Model):
  entity = models.ForeignKey(Entity)

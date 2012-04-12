"""
Argument List
  setup : setup db

Qpition list:
  -h : show this message
  -t : testing config
"""

import os, sys
from lxml import etree
os.path.join(os.path.abspath('..'), 'sydneymenu', 'main')
sys.path.append(os.path.join(os.path.abspath('..'), 'sydneymenu', 'main'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from main.core.models import EntityConfig 
from main.pybb.models import Forum,Category
from main.core import xmlbase
from main.glue.forum import AddForum 
from main.glue.forum import DeleteForum 
import json
import os
import getopt
import sys

def CleanData(version):
  from django.db import connection, transaction
  cursor = connection.cursor()
  cursor.execute("DELETE FROM core_info where version<%s",[version])
  transaction.commit_unless_managed()

def InitEntityConfig(name):
  config = None
  try:
    config = EntityConfig.objects.get(name=name)
  except EntityConfig.DoesNotExist:
    config = EntityConfig() 
    config.version = 0
  try:
    old_version = config.version
    xslt_io = open ("./config/" + name + ".xslt")
    xsd_io = open("./config/" + name + ".xsd")
    xsd_io2 = open("./config/" + name + ".xsd")
    print ("Set Extension:" + name)
    xmlbase.SetExtension(config,name,xslt_io,xsd_io)
    print "testing rending ..."
    rslt = config.GetXSLT()
    form = xmlbase.FormFromXSD('item',etree.parse(xsd_io2))
    print form
    #print "Clean data in info before version %s" % config.version
    #CleanData(default.version)
    return True
  except etree.XMLSyntaxError,e:
    print e
    return False
  finally:
    xslt_io.close()
    xsd_io.close()
    xsd_io2.close()
 

def InitForum():
  try:
    get_category = Category.objects.get(name='Services')
  except Category.DoesNotExist:
    category_record = Category(name='Services')
    category_record.save()
  try:
    get_category = Category.objects.get(name='Issues')
  except Category.DoesNotExist:
    category_record = Category(name='Issues')
    category_record.save()
  try:
    get_category = Category.objects.get(name='Technical Support')
  except Category.DoesNotExist:
    category_record = Category(name='Technical Support')
    category_record.save()
  DeleteForum('Bug Report')
  AddForum('Issues','Bug Report')
  DeleteForum('FAQ')
  AddForum('Technical Support','FAQ')
  print 'Forum Bug Report created'

    
def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:],"ht",["help","test"])
  except getopt.error, msg:
    print msg
    print "for help use --help"
    exit(1)
  for o, a in opts:
    if o in ("-h","--help"):
      print __doc__
      sys.exit(0)
    elif o in ("-t","--test"):
      InitEntityConfig('default')
      InitEntityConfig('plant')
      sys.exit(0)
  for arg in args:
    if arg == "setup":
      InitEntityConfig('default')
      InitEntityConfig('plant')
      InitForum()
      print 'Database has been initialized'
      sys.exit(0)
    elif arg == "forum":
      InitForum()
      print 'Forum has been initialized'
      sys.exit(0)
  print ("Argument is not provided.\n")
  sys.exit(1)

if __name__ == "__main__":
  main()

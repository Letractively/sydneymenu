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

from main.core.models import ServiceConfig 
from main.pybb.models import Forum,Category
from main.core import xmlbase
import json
import os
import getopt
import sys

def CleanData(version):
  from django.db import connection, transaction
  cursor = connection.cursor()
  cursor.execute("DELETE FROM core_info where version<%s",[version])
  transaction.commit_unless_managed()

def InitServiceConfig():
  default = None
  try:
    default = ServiceConfig.objects.get(name='default')
  except ServiceConfig.DoesNotExist:
    default = ServiceConfig() 
    default.version = 0
  try:
    old_version = default.version
    xslt_io = open ("./config/default.xslt")
    xsd_io = open("./config/default.xsd")
    xsd_io2 = open("./config/default.xsd")
    test_io = open("./config/test.xml") 
    print "Set Default Extension:"
    xmlbase.SetExtension(default,'default',xslt_io,xsd_io)
    print "Initial default Service Config Successful"
    print "testing rending ..."
    test_doc = etree.parse(test_io)
    rslt = default.GetXSLT()
    print etree.tostring(rslt(test_doc.getroot()[0]).getroot(),pretty_print = True)
    form = xmlbase.FormFromXSD('item',etree.parse(xsd_io2))
    print form
    print "Clean data in info before version %s" % default.version
    #CleanData(default.version)
    return True
  except etree.XMLSyntaxError,e:
    print e
    return False
  finally:
    xslt_io.close()
    xsd_io.close()
    xsd_io2.close()
    test_io.close()
 

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
    print 'Initial record has been inserted'

    
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
      if InitServiceConfig():
        sys.exit(0)
      else:
        sys.exit(1)
  for arg in args:
    if arg == "setup":
      InitServiceConfig()
      InitForum()
      print 'Database has been initialized'
      sys.exit(0)
  print ("Argument is not provided.\n")
  sys.exit(1)

if __name__ == "__main__":
  main()

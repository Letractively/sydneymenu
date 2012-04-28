"""
Argument List
  garden : clean all the gardens 
"""

import os, sys
from lxml import etree
path = os.path.join(os.path.abspath('../..'),)
sys.path.append(path)

path = os.path.join(os.path.abspath('../..'),"main")
sys.path.append(path)

print path

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from main.core.models import EntityConfig 
from main.core.models import Entity 
from main.core import xmlbase
import json
import os
import getopt
import sys

def CleanGarden():
  entities = Entity.objects.filter(category = 'garden')
  for entity in entities:
    entity.Clean()
    Entity.delete(entity)
    print (entity.name + " has been deleted")
    
def main():
  try:
    opts, args = getopt.getopt(sys.argv[1:],"h")
  except getopt.error, msg:
    print msg
    print "for help use --help"
    exit(1)
  for arg in args:
    if arg == "garden":
      CleanGarden()
      print 'All service entities has been deleted'
      sys.exit(0)
  print ("Argument is not provided.\n")
  sys.exit(1)

if __name__ == "__main__":
  main()

import sys
import re
import os
from shutil import rmtree
from shutil import copytree
from lxml import etree
from datetime import date 
from datetime import datetime
from config import *


def SaveConfig(sname,node):
  os.remove(CONFIG.SERVICES_PATH + sname+'/config.xml')
  fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_CREAT|os.O_WRONLY)
  os.write(fd,etree.tostring(node,pretty_print = True))
  os.close(fd)

def InitNode(node,path,name):
  al = node.xpath("./"+path)
  an = None
  if (len (al) == 0):
    an = etree.Element(name)
    node.append(an)
    return an
  else:
    an = al[0]
    return an

# We need a general xml handler here #
#class XMLNodeProx:
#  def InitProx(path,lef,key):

class Layout:
  @staticmethod
  def InitLayoutConfig(node):
    return Layout(InitNode(node,"LAYOUT","LAYOUT"))

  def __init__(self,node):
    self.gnode = node

  def LeftNode(self):
    return InitNode(self.gnode,"LEFT","LEFT")

  def RightNode(self):
    return InitNode(self.gnode,"RIGHT","RIGHT")

  def MidNode(self):
    return InitNode(self.gnode,"MID","MID")

  def SaveLayout(self,ldict):
    for a in self.gnode.xpath("./LEFT"):
      self.gnode.remove(a)
    for a in self.gnode.xpath("./MID"):
      self.gnode.remove(a)
    for a in self.gnode.xpath("./RIGHT"):
      self.gnode.remove(a)
    lnode = InitNode(self.gnode,"LEFT","LEFT")
    for v in ldict['left']:
       n = InitNode(lnode,v,v)
    mnode = InitNode(self.gnode,"MID","MID")
    for v in ldict['middle']:
       n = InitNode(mnode,v,v)
    rnode = InitNode(self.gnode,"RIGHT","RIGHT")
    for v in ldict['right']:
       n = InitNode(rnode,v,v)
    return self.gnode

  def GetLayout(self):
    ldict = {'LEFT':[],'MID':[],'RIGHT':[]}
    lnode = InitNode(self.gnode,"LEFT","LEFT")
    for v in lnode.getchildren():
      ldict['LEFT'].append(v.tag)
    mnode = InitNode(self.gnode,"MID","MID")
    for v in mnode.getchildren():
      ldict['MID'].append(v.tag)
    rnode = InitNode(self.gnode,"RIGHT","RIGHT")
    for v in rnode.getchildren():
      ldict['RIGHT'].append(v.tag)
    return ldict


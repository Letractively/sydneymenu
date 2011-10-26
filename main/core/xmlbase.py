import sys
import re
import os
from shutil import rmtree
from shutil import copytree
from lxml import etree
from datetime import date 
from datetime import datetime
from config import *
from models import *


def SaveConfig(sname,node):
  os.remove(CONFIG.SERVICES_PATH + sname+'/config.xml')
  fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_CREAT|os.O_WRONLY)
  os.write(fd,etree.tostring(node,pretty_print = True))
  os.close(fd)

def SetExtension(ext,ext_name,xslt_str,xsd_str):
  xsd_doc = etree.parse(xsd_str) 
  xslt_doc = etree.parse(xslt_str)
  schema = etree.XMLSchema(xsd_doc)
  xslt = etree.XSLT(xslt_doc)
  # make sure the ext_name has not been used
  ext.name = ext_name 
  ext.xslt = etree.tostring(xslt_doc.getroot(),pretty_print = True) 
  ext.xsd = etree.tostring(xsd_doc.getroot(),pretty_print = True)
  ext.version = 0
  ext.save()

def ModifyExtension(ext_name,xslt_str,xsd_str):
  try:
    ext = ServiceConfig.objects.get(name = ext_name)
    xsd_doc = etree.parse(xsd_str) 
    xslt_doc = etree.parse(xslt_str)
    schema = etree.XMLSchema(xsd_doc)
    xslt = etree.XSLT(xslt_doc)
    ext.xslt = xslt_str
    ext.xsd = xsd_str
    ext.version = ext.version + 1 
    ext.save()
    return ext 
  except ServiceConfig.DoesNotExist:
    return None #Does not return any usefull info, run check.py
  except:
    return None #Does not return any usefull info, run check.py

def FormFromXSD(path,xsd):
  # make sure there is no exception throw here, runing test before put it into use
  try:
    form_xslt_io = open(CONFIG.XSLT_FORM_PATH)
    xslt_doc = etree.parse(form_xslt_io)
    xslt = etree.XSLT(xslt_doc)
    form = xslt(xsd,name="'"+path+"'")
    return form 
  finally:
    form_xslt_io.close()

def XMLTemplateFromXSD(path,xsd):
  # make sure there is no exception throw here, runiing test before put it into use
  template_xslt_io = None
  try:
    template_xslt_io = open(CONFIG.XSLT_TEMPLATE_PATH)
    xslt_doc = etree.parse(template_xslt_io)
    xslt = etree.XSLT(xslt_doc)
    template = xslt(xsd,name="'"+path+"'")
    return template
  finally:
    if template_xslt_io:
      template_xslt_io.close()

def CreateNewInfo(service,xml_str,path):
  xsd_doc = service.extend.GetXSDDoc()
  schema = etree.XMLSchema(xsd_doc)
  xml_doc = etree.parse(StringIO(xml_str))
  schema.assertValid(xml_doc)
  info = Info()
  info.version = service.extend.version
  info.path = path
  info.service = service.name 
  info.data = xml_str
  info.save()
  return info

def ModifyInfo(service,xml_str,path,id):
  xsd_doc = service.extend.GetXSDDoc()
  schema = etree.XMLSchema(xsd_doc)
  xml_doc = etree.parse(StringIO(xml_str))
  schema.assertValid(xml_doc)
  info = Info.objects.get(id=id)
  info.version = service.extend.version
  info.path = path
  info.service = service.name 
  info.data = xml_str
  info.save()
  return info



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


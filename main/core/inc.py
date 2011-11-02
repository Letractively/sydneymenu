from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page,cache_control
from django.utils.http import urlquote
from django.utils.http import urlencode
from urllib import unquote
from models import *
from patten import *
from config import *
from xmlbase import *
import json
import math
import mimetypes

mimetypes.init()

def session_prefix(handler):
  def rst_handler(request,*args):
    request.session.set_expiry(0)
    return handler(request,*args)
  return rst_handler

def ErrorRes(request):
  if (request.REQUEST.has_key('cache')):
    fd = open(CONFIG.RES_PATH + 'res_error.png')
    mime_type_guess = mimetypes.guess_type('res_error.png')
    response = HttpResponse(fd,mimetype = mime_type_guess[0])
    return response
  else:
    return HttpResponseRedirect('/res/res_error.png')

class NodeAlreadyExist:
  pass

def GetService(s_name):  
  try:
      service_data = ServiceCore.objects.get(name = s_name)
      return service_data
  except ServiceCore.DoesNotExist:
      return None

def Rad(x):
  return math.radians(x)

def ComputeDistance(latlong1,latlong2):
  r = 6371
  dlat = Rad(latlong1['lat'] - latlong2['lat'])
  dlong = Rad(latlong1['long'] - latlong2['long'])
  a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(Rad(latlong1['lat']))*math.cos(Rad(latlong2['lat']))*math.sin(dlong/2)*math.sin(dlong/2)
  c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a));
  return r*c 

def GetCacheData(sname):
  gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml').getroot()
  cache = InitNode(gnode,'CACHE','CACHE')
  old_type = cache.get('type')
  if(old_type):
    f = open(CONFIG.SERVICES_PATH + sname + '/cache.' + old_type,'r')
    data = f.read()
    f.close()
    return {'data':data,'type':old_type}
  else:
    return None

def SaveCacheData(sname,data,t):
  gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml').getroot()
  cache = InitNode(gnode,'CACHE','CACHE')
  old_type = cache.get('type')
  if (old_type):
    try:
      os.remove(CONFIG.SERVICES_PATH + sname + '/cache.' + old_type)
    except os.error:
      pass
  cache.set('type',t)
  fd = os.open(CONFIG.SERVICES_PATH + sname + '/cache.' + t,os.O_RDWR|os.O_CREAT)
  os.write(fd,data)
  os.close(fd)
  SaveConfig(sname,gnode)

def GeneralXMLResponse(request,command_error,msg=None):
    general_t = loader.get_template('core/__general_result.xml')
    c = {'REQUEST':request.REQUEST}
    if (command_error):
      c['ERROR'] = command_error
    if (msg):
      c['MSG'] = msg
    now = datetime.now()
    tstamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    c['TIME_STAMP'] = tstamp
    response =  HttpResponse(general_t.render(Context(c)),mimetype = "text/xml")
    response['Cache-Control'] = 'no-cache'
    return response

class PhotoPlay:
  @staticmethod
  def InitPhotoPlayConfig(node):
    return PhotoPlay(InitNode(node,"PHOTOS","PHOTOS"))

  def __init__(self,node):
    self.gnode = node

  def BasicInfo(self):
    return self.gnode.get("gallery")

class Gallery:
  @staticmethod
  def InitGalleryConfig(node):
    return Gallery(InitNode(node,"GALLERY","GALLERY"))
  
  def __init__(self,node):
    self.gnode = node
  
  def GetAll(self):
    gnames = []
    for a in self.gnode.xpath("//G"):
      gnames.push(a.get('name'))
    return gnames

  def BasicInfo(self):
    g = {}
    for a in self.gnode.xpath("//G"):
      rs = a.xpath("./IMG")
      g[a.get('name')] = []
      for v in rs:
        g[a.get('name')].append(v.get('name'))
    return g
  
  def XML(self):
    return etree.tostring(self.gnode,pretty_print = True)

  def SetGalleryName(self,name,n_name):
    nodes = self.gnode.xpath("//G[@name='"+name+"']")
    if (len (nodes) == 0):
      nodes[0].set('name',n_name)
      return node[0]
    else:
      return None

  def AddGallery(self,name):
    nodes = self.gnode.xpath("./G[@name='"+name+"']")
    if (len (nodes) == 0):
      gn = etree.Element("G",name = name)
      self.gnode.append(gn)
      return gn
    else:
      raise NodeAlreadyExist

  def RemoveGallery(self,name):
    nodes = self.gnode.xpath("//G[@name = '"+name+"']")
    for n in nodes:
      self.gnode.remove(n)

  def AddImage(self,gname,iname,url):
    nodes = self.gnode.xpath("//G[@name='"+gname+"']")
    img = etree.Element("IMG",name=iname,url = url)
    if (len(nodes) == 0):
      g = etree.Element("G",name=gname)
      g.append(img)
      self.gnode.append(g)
      return img
    else:
      imgs = nodes[0].xpath("./IMG[@name='"+iname+"']")
      if(len(imgs)==0):
        nodes[0].append(img)
        return img
      else:
        return None
  
  def HasGallery(self,gname):
    nodes = self.gnode.xpath("//G[@name='"+gname+"']")
    if (len(nodes) == 0):
        return False
    else:
        return True;

  def GetImageFile(self,gname,iname):
    nodes = self.gnode.xpath("//G[@name='"+gname+"']/IMG[@name='"+iname+"']")
    if (len(nodes) == 0):
      return None
    else:
      return nodes[0].get('url')
      
  def SetImagePath(self,path,url):
    names = path.split('/')
    if (len(names) == 2):
      iname = names[1]
      gname = names[0]
      nodes = self.gnode.xpath("//G[@name='"+gname+"']/IMG[@name='"+iname+"']")
      if(len (nodes) == 1):
        nodes[0].set("url",url)
        return nodes[0] 
      else:
        return None 
    else:
      return None 

def InitServiceDir(s_name,data = None):
    copytree(CONFIG.SERVICES_PATH + 'init',CONFIG.SERVICES_PATH + s_name)
    if (data):
      os.remove(CONFIG.SERVICES_PATH + s_name + '/icon.png')
      #FIX ME:following code should read data type
      #fd = os.open(CONFIG.SERVICES_PATH + s_name + '/icon.' + data['type'],os.O_RDWR | os.O_CREAT)
      fd = os.open(CONFIG.SERVICES_PATH + s_name + '/icon.png',os.O_RDWR | os.O_CREAT)
      os.write(fd,data['data'])
      os.close(fd)

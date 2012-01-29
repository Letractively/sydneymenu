from user import * 
from glue.forum import *
from django.views.decorators.csrf import csrf_exempt
import logging

# NOTICE: This is the top level module, do not import this file.

def CrunchImage(folder,img_name,cache_data,crunch):
  img_full_path = folder+'/' + img_name+'.' + cache_data['type'];
  img_sc_full_path = folder+'/' + "sc_" + img_name + "." + cache_data['type'];
  im = cache_data['data']
  w,h = im.size
  sw = w*crunch['wp']
  sh = h*crunch['hp']
  st = h*crunch['top']
  sl = w*crunch['left']
  crop = im.crop((int(sl),int(st),int(sw+sl),int(st+sh)))
  p = 1
  if(sw > 200):
    p = float(200)/sw
  if(p > 200/sh):
    p =float(200)/sh 
  crop = crop.resize((int(sw*p),int(sh*p)),Image.ANTIALIAS)
  crop.save(img_sc_full_path)

def BuildCrunch(request):
  dic = request.REQUEST
  crunch = {'top':0,'left':0,'wp':1,'hp':1}
  if(dic.has_key('top')):
    crunch['top'] = (GetFloat(dic['top']) or 0)/10000
  if(dic.has_key('left')):
    crunch['left'] = (GetFloat(dic['left']) or 0 )/10000
  if(dic.has_key('wp')):
    crunch['wp'] = (GetFloat(dic['wp']) or 10000)/10000
  if(dic.has_key('hp')):
    crunch['hp'] = (GetFloat(dic['hp']) or 10000)/10000
  return crunch

def ImageLink(request,sname,respath):
    def SuccReplyMessage(url):
      return "<RESURL>"+url+"</RESURL> updated successfully"
    aut = HasAuthority(request,sname)
    action = 'default'
    if(request.REQUEST.has_key('action')):
      action = request.REQUEST['action']
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    path = respath.split('/')
    resname = path.pop()
    gname = ''
    if path:
      gname = path.pop()
    else:
      command_error['INVALID'] = "INVALID GALLERY NAME"
      return GeneralXMLResponse(request,command_error,'No Authority')
    data = aut['s']
    crunch = {}
    if(request.REQUEST.has_key('vflip')):
      crunch['vflip'] = True
    if(request.REQUEST.has_key('hflip')):
      crunch['hflip'] = True
    if(request.REQUEST.has_key('rotation') and request.REQUEST['rotation'].isdigit()):
      crunch['rotation'] = int(request.REQUEST['rotation'])
    if(data.activate == True):
      gnode = GetConfigDoc(sname)
      gallery = Gallery.InitGalleryConfig(gnode)
      old_file_name = gallery.GetImageFile(gname,resname)
      if (old_file_name == None):
        newname = resname 
        if(request.REQUEST.has_key('rename')):
          newname = request.REQUEST['rename']
        cache_data = GetCacheData(sname,crunch)
        if cache_data:
            image_type = cache_data['type']
            fname = newname + '.' + image_type
            node = gallery.AddImage(gname,newname,fname)
            if(node == None):
              command_error['MISC'] = 'RES ALREADY EXIST,'+gname+'/'+newname+'/'
              return GeneralXMLResponse(request,command_error)
            else:
              fd = open(CONFIG.SERVICES_PATH + sname + '/' + gname + "/" + fname,'a')
              cache_data['data'].save(fd,cache_data['data'].format)
              fd.close()
              CrunchImage(CONFIG.SERVICES_PATH + sname + '/' + gname,newname,cache_data,BuildCrunch(request))
              SaveConfig(sname,gnode)
              HistoryHelper.Record(request,aut['s'].name,"IMAGE_ADD",gname)
              return GeneralXMLResponse(request,command_error,SuccReplyMessage(gname + '/' + newname))
        else:
          command_error['MISC'] = 'No Cache Data Found'
          return GeneralXMLResponse(request,command_error)
      else:
        if (action == 'add'):
          command_error['MISC'] = 'Resource ' + respath + " already exist"
          return GeneralXMLResponse(request,command_error)
        newname = resname 
        if(request.REQUEST.has_key('rename')):
          newname = request.REQUEST['rename']
        if (newname != resname): #if rename to a different name
          if(gallery.GetImageFile(gname,newname)):
            command_error['MISC'] = 'Resource ' + newname + ' already exist'
            return GeneralXMLResponse(request,command_error)
        cache_data = GetCacheData(sname,crunch)
        if cache_data:
          image_type = cache_data['type']
          fname = newname + '.' + image_type
          node = gallery.SetImagePath(respath,fname,newname)
          if(node == None):
            command_error['MISC'] = 'RES NOT EXIST'
            return GeneralXMLResponse(request,command_error)
          try:
            os.remove(CONFIG.SERVICES_PATH + sname + '/' + gname+ '/' + old_file_name)
          except os.error:
            pass
          fd = open(CONFIG.SERVICES_PATH + sname + '/' + gname + "/" + fname,'a')
          cache_data['data'].save(fd,cache_data['data'].format)
          fd.close() 
          CrunchImage(CONFIG.SERVICES_PATH + sname + '/' + gname,newname,cache_data,BuildCrunch(request))
          SaveConfig(sname,gnode)
          return GeneralXMLResponse(request,command_error,SuccReplyMessage(gname + '/' + newname))
        else:
          command_error['MISC'] = 'No Cache Data Found'
          return GeneralXMLResponse(request,command_error)
    else:
        command_error['MISC'] = 'SERVICE NOT ACTIVATED'
        return GeneralXMLResponse(request,command_error,"no resource added")


def GetGallery(request,sname):
    try:
      data = ServiceCore.objects.get(name = sname)
      if (data.activate == True):
        fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_RDWR)
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        return HttpResponse(gallery.XML(),mimetype = "text/xml")
      else:
        return HttpResponse("<FAIL>Service not activated</FAIL>") 
    except ServiceCore.DoesNotExist:
        return HttpResponse("<FAIL>Service not existed</FAIL>")

def ImageCache(request,sname,method):
    service = GetService(sname)
    reqdic = request.REQUEST
    if (service == None):
      return HttpResponse('Service Not Exist')
    if request.FILES.has_key('cache'):
      f = request.FILES['cache'].name
      ns = f.split('.')
      image_type = ns[len(ns)-1]
      data = request.FILES['cache'].read()
      SaveCacheData(sname,data,image_type)
    if (method =='data'):
      crunch = {}
      if(request.REQUEST.has_key('vflip')):
        crunch['vflip'] = True
      if(request.REQUEST.has_key('hflip')):
        crunch['hflip'] = True
      if(request.REQUEST.has_key('rotation') and request.REQUEST['rotation'].isdigit()):
        crunch['rotation'] = int(request.REQUEST['rotation'])
      cache_data = GetCacheData(sname,crunch)
      if(cache_data):
        response = HttpResponse(mimetype = "image/"+cache_data['type'])
        cache_data['data'].save(response,cache_data['data'].format)
        return response 
      else:
        return HttpResponseRedirect('/res/dft_icon.png');
    else:
      return HttpResponse("ok");

def Icon(request,sname,path):
    try:
      data = Info.objects.get(path=path,service = sname)
      doc = data.GetDataDoc()
      path = doc.xpath("//icon/@path")[0]
      return HttpResponseRedirect('/gallery/image/'+sname+'/'+path + '/?sc=true')
    except Info.DoesNotExist:
      return HttpResponseRedirect('/res/dft_icon.png');
      
    

@cache_page(0)
def Resource(request,sname,res):      
    try:
      data = ServiceCore.objects.get(name = sname)
      gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
      rs = res.split('/')
      url = None
      if(len(rs) == 1):
        urls = gnode.getroot().xpath("./IMG[@name='"+res+"']")
        if(len(urls) == 0):
          return ErrorRes(request)
        else:
          url = urls[0].get('url')
          if(request.REQUEST.has_key('sc')):
            url = "sc_"+url; 
      else:
        gname = rs[0]
        iname = rs[1]
        gallery = Gallery.InitGalleryConfig(gnode.getroot()) 
        path = gallery.GetImageFile(gname,iname)
        if(path == None):
          return HttpResponseRedirect('/res/res_error.png')
        else:
          if(request.REQUEST.has_key('sc')):
            url = gname + '/sc_' + path
          else:
            url = gname + '/' + path
      fd = open(CONFIG.SERVICES_PATH + sname+'/'+url,'r')
      mime_type_guess = mimetypes.guess_type(url)
      data = fd.read()
      fd.close()
      response = HttpResponse(data,mimetype = mime_type_guess[0])
      if (request.REQUEST.has_key('cache')):
        response['Cache-Control'] = 'max-age'
      else:
        response['Cache-Control'] = 'no-cache'
      return response
    except ServiceCore.DoesNotExist:
      return HttpResponseRedirect('/res/res_error.png')

def GalleryInfo(request,sname):
    try:
      data = ServiceCore.objects.get(name = sname)
      if (data.activate == True):
        fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_RDWR)
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        return HttpResponse(gallery.XML(),mimetype = "text/xml")
      else:
        return HttpResponse("<FAIL>Service not activated</FAIL>") 
    except ServiceCore.DoesNotExist:
        return HttpResponse("<FAIL>Service not existed</FAIL>")

def Rename(request,sname,gname,n_gname):
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        return HttpResponse(aut['m'])
    data = ServiceCore.objects.get(name = sname)
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        if (gallery.SetGalleryName(gname,n_gname)):
          fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_RDWR)
          os.write(fd,etree.tostring(gnode,pretty_print = True))
          os.close(fd)
          return HttpResponse("Gallery Renamed")
        else:
          return HttpResponse("Gallery Not Found")
    else:
        return HttpResponse("Service Not Activated") 

def Add(request,sname):
    command_error = {}
    aut = HasAuthority(request,sname)
    gallery_attr = {}
    command_error = model_obj_builder(gallery_attr,request.REQUEST,addgallery_handler)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = aut['s']
    if (data.activate == True):
        gname = gallery_attr['name']
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        try:
          gallery.AddGallery(gname)
          os.mkdir(CONFIG.SERVICES_PATH + sname + '/' + gname)
          SaveConfig(sname,gnode)
          return GeneralXMLResponse(request,command_error,"Gallery " +gname +"  Created Successfully")
        except NodeAlreadyExist:
          command_error['MISC'] = "COMMAND FAIL, Gallery " + gname + " Already Exist"
          return GeneralXMLResponse(request,command_error,"Gallery " +gname +" Not  Created")
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error,"Gallery Not Created")

def Remove(request,sname,gname):
    command_error = {}
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error,'You Have No Authority To Do This.')
    else:
        data = aut['s']
        if(data.activate == True):
          gnode = etree.parse(CONFIG.SERVICES_PATH + sname + '/config.xml')
          gallery = Gallery.InitGalleryConfig(gnode.getroot())
          gallery.RemoveGallery(gname)
          SaveConfig(sname,gnode)
          rmtree(CONFIG.SERVICES_PATH + sname+'/'+gname)
          return GeneralXMLResponse(request,command_error,"Gallery " +gname +"  Removed Successfully")
        else:
          command_error['MISC'] = "SERVICE NOT ACTIVATED"
          return GeneralXMLResponse(request,command_error,"Gallery " +gname +" Not  Deleted")


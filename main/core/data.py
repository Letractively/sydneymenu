from user import * 
from glue.forum import *
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import logging
# NOTICE: This is the top level module, do not import this file.

def CrunchImage(folder,img_name,img_type):
  img_full_path = folder+'/' + img_name+'.' + img_type;
  img_sc_full_path = folder+'/' + "sc_" + img_name + "." + img_type;
  im = Image.open(img_full_path)
  w,h = im.size
  sqsize = min(w,h)
  crop = im.crop((0,0,sqsize,sqsize))
  if(sqsize>150):
    crop = crop.resize((150,150),Image.ANTIALIAS)
  crop.save(img_sc_full_path)

def Report(request):
  command_error = {}
  r_data = {}
  command_error = model_obj_builder(r_data,request.REQUEST,report_handler)
  if command_error:
    return GeneralXMLResponse(request,command_error,"Invalid Infomation Provided")
  else:
    info = """["%s",%d,%d,"%s"]"""%(urlquote(r_data['address']),
          r_data['latitude'],r_data['longitude'],urlquote(r_data['type']))
    HistoryHelper.Record(request,r_data['name'],"REPORT",info)
    return GeneralXMLResponse(request,command_error,"Thank You For Sharing Your Valuable Experience!")

def RemoveService(request,sname):
  aut = HasAuthority(request,sname)
  command_error = {}
  if (aut['r'] == False):
      command_error['AUTHORITY'] = 'NO_AUTHORITY'
      return GeneralXMLResponse(request,command_error)
  try:
      data = aut['s']
      try:
        rmtree(CONFIG.SERVICES_PATH+sname)
      except OSError:
        pass
      ServiceCore.delete(data)
      DeleteForum(sname)
      return GeneralXMLResponse(request,command_error,'Service Removed Successfully')
  except ServiceCore.DoesNotExist:
      command_error['MISC'] = 'Service Does Not Exist'
      return GeneralXMLResponse(request,command_error)

def ResetService(request,name):
    aut = HasAuthority(request,name)
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    try:
        data = ServiceCore.objects.get(name = name)
        if (data.activate == True):
            rmtree(CONFIG.SERVICES_PATH+name)
            InitServiceDir(name)
            return GeneralXMLResponse(request,command_error,'Service Reset Successfully')
        else:
            command_error['MISC'] = 'Service Not Activated'
            return GeneralXMLResponse(request,command_error)
    except ServiceCore.DoesNotExist:
        command_error['MISC'] = 'Service Does Not Exist'
        return GeneralXMLResponse(request,command_error)

def AddService(request):
# Need to build the Error Code and Generate A Replay XML If failed
# If all the info are collected, return a Successful html page.
    s_data = ServiceCore()
    command_error = model_obj_builder(s_data,request.REQUEST,addserv_handler)
    s_data.grade = 1
    s_data.privilege = 'normal'
    s_data.activate = True
    rel = ServiceRel.objects.get(name='undefined')
    s_data.extend = rel
    Permission.CreateService(request,s_data,command_error)
    if command_error:
        service_t = loader.get_template('core/__addservice_fail.xml')
        c = Context({'REQUEST':request.REQUEST,'ERROR':command_error})
        return HttpResponse(service_t.render(c),mimetype = "text/xml")
    else:
        try:
          fail_t = loader.get_template('core/__addservice_conflict.xml')
          old_name_data = ServiceCore.objects.get(name=s_data.name)
          command_error['name'] = "Service Name Already Used"
          return GeneralXMLResponse(request,command_error)
        except ServiceCore.DoesNotExist:
          if(not IsSystem(request)):
            try:
              old_mail_data = ServiceCore.objects.get(email=s_data.email)
              command_error['email'] = "Email Already Used"
              return GeneralXMLResponse(request,command_error)
            except ServiceCore.DoesNotExist:
              pass
          else:
            pass          
        try:
          s_data.full_clean()
          s_data.save()
          sname = s_data.name
          InitServiceDir(sname,None)
          CrunchImage(CONFIG.SERVICES_PATH + sname,'icon','png')
          service_t = loader.get_template('core/__addservice_succ.xml')
          c = Context({'REQUEST':request.REQUEST})
          return HttpResponse(service_t.render(c),mimetype = "text/xml")
        except ValidationError, e:
          service_t = loader.get_template('core/__addservice_fail.xml')
          c = Context({'REQUEST':request.REQUEST,'ERROR':e.message_dict})
          return HttpResponse(service_t.render(c),mimetype = "text/xml")

def ModifyService(request,sname):
    aut = HasAuthority(request,sname)
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    s_data = aut['s']
    command_error = model_obj_builder(s_data,request.REQUEST,mdyserv_handler)
    if command_error:
        return GeneralXMLResponse(request,command_error)
    else:
        try:
          s_data.full_clean()
          s_data.save()
          return GeneralXMLResponse(request,command_error,'Service Info Has Been Updated')
        except ValidationError, e:
          command_error['MISC'] = "Unknow Error, Can Not Save Data"
          return GeneralXMLResponse(request,command_error,'Unknow Error!! Please Check The Input Carefully')

def GetServices(request):
# The get service will always provides all the services
    services = ServiceCore.objects.all()
    reports = History.objects.filter(type="REPORT")
    data_t = loader.get_template('core/__getservices.xml')
    c = Context({'SERVICES':services,"REPORTS":reports})
    response = HttpResponse(data_t.render(c),mimetype = "text/xml")
    response['Cache-Control'] = 'no-cache'
    return response

def ActivateService(request,name):
    try:
        data = ServiceCore.objects.get(name = name)
        if (data.activate == True):
            return HttpResponse("Service Already Activated")
        else:
            data.activate = True
            data.save()
            return HttpResponse("Service Activated")
    except ServiceCore.DoesNotExist:
        return HttpResponse("Service Does Not Exist")

def ImageLink(request,sname,rname):
    aut = HasAuthority(request,sname)
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    cache_data = GetCacheData(sname)
    if cache_data:
        image_type = cache_data['type']
        data = aut['s']
        if(data.activate == True):
          gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
          rs = rname.split('/')
          url = None
          if(len(rs) == 1):
            iname = rs[0]
            urls = gnode.getroot().xpath("./IMG[@name='"+iname+"']")
            if(len(urls) == 0):
              command_error['MISC'] = 'RES PATH ERROR'
              return GeneralXMLResponse(request,command_error)
            else:
              url = urls[0].get('name')+'.'+ image_type
              try:
                os.remove(CONFIG.SERVICES_PATH + sname + '/' + urls[0].get('url'))
              except os.error:
                pass
              fd = os.open(CONFIG.SERVICES_PATH + sname + '/' + url,os.O_RDWR|os.O_CREAT)
              os.write(fd,cache_data['data'])
              os.close(fd)
              CrunchImage(CONFIG.SERVICES_PATH + sname,iname,image_type)
              urls[0].set('url',url)
              SaveConfig(sname,gnode)
              return GeneralXMLResponse(request,command_error,'resource was added successfully')
          else:
            gname = rs[0]
            iname = rs[1]
            url = iname + '.' + image_type;
            gallery = Gallery.InitGalleryConfig(gnode.getroot())
            o_url = gallery.GetImageFile(gname,iname)
            node = gallery.SetImagePath(rname,url)
            if(node == None):
              command_error['MISC'] = 'RES NOT EXIST'
              return GeneralXMLResponse(request,command_error)
            else:
              try:
                os.remove(CONFIG.SERVICES_PATH + sname + '/' + gname+ '/' + o_url)
              except os.error:
                pass
              fd = os.open(CONFIG.SERVICES_PATH + sname + '/' + gname + "/" + url,os.O_RDWR|os.O_CREAT)
              os.write(fd,cache_data['data'])
              os.close(fd)
              CrunchImage(CONFIG.SERVICES_PATH + sname + '/' + gname,iname,image_type)
              SaveConfig(sname,gnode)
              return GeneralXMLResponse(request,command_error,'resource was added successfully')
        else:
          command_error['MISC'] = 'SERVICE NOT ACTIVATED'
          return GeneralXMLResponse(request,command_error,"no resource added")
    else:
        command_error['MISC'] = 'RES NOT EXIST'
        return GeneralXMLResponse(request,command_error)

def ImageAdd(request,sname,rname):
    aut = HasAuthority(request,sname)
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error,aut['m'])
    cache_data = GetCacheData(sname)
    if cache_data:
        data = aut['s']
        if(data.activate == True):
          gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
          rs = rname.split('/')
          url = None
          if(len(rs) == 1):
            command_error['MISC'] = 'RES PATH ERROR'
            return GeneralXMLResponse(request,command_error)
          else:
            gallery = Gallery.InitGalleryConfig(gnode.getroot())
            gname = rs[0]
            iname = rs[1]
            image_type = cache_data['type']
            url = iname + '.' + image_type;
            node = gallery.AddImage(gname,iname,url)
            if(node == None):
              command_error['MISC'] = 'RES ALREADY EXIST,'+gname+'/'+iname+'/'+url
              return GeneralXMLResponse(request,command_error)
            else:
              fd = os.open(CONFIG.SERVICES_PATH + sname + '/' + gname + "/" + url,os.O_RDWR|os.O_CREAT)
              os.write(fd,cache_data['data'])
              os.close(fd)
              CrunchImage(CONFIG.SERVICES_PATH + sname + '/' + gname,iname,image_type)
              SaveConfig(sname,gnode)
              HistoryHelper.Record(request,aut['s'].name,"IMAGE_ADD",gname)
              return GeneralXMLResponse(request,command_error,'resource was added successfully')
    else:
        command_error['MISC'] = 'CAN NOT FOUND CACHE DATA'
        return GeneralXMLResponse(request,command_error)

def ImageCache(request,sname,method):
    service = GetService(sname)
    if (service == None):
      return HttpResponse('Service Not Exist')
    if request.FILES.has_key('cache'):
      f = request.FILES['cache'].name
      ns = f.split('.')
      image_type = ns[len(ns)-1]
      data = request.FILES['cache'].read()
      SaveCacheData(sname,data,image_type)
    if (method =='data'):
      data = GetCacheData(sname)
      if(data):
        return HttpResponse(data['data'],
          mimetype = "image/"+data['type'])
      else:
        return HttpResponseRedirect('/res/dft_icon.png');
    else:
      return HttpResponse("ok");

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








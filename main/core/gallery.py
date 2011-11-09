from user import *
#NOTICE: This is the top level module, do not import this file

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

def Play(request,sname):
    play_t = loader.get_template('comp/photoplayer.html')
    data = ServiceCore.objects.get(name = sname)
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        gname = gallery.GetDefault()
        if(gname):
          c = Context({'GALLERY':gallery.BasicInfo()[gname]})
          return HttpResponse(play_t.render(c),mimetype="text/html")
        else:
          return HttpResponse("Default Gallery Not Specified")
    else:
        return HttpResponse("Service Not Activated") 


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

def Default(request,sname,gname):
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        return HttpResponse(aut['m'])
    data = ServiceCore.objects.get(name = sname)
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        if gallery.SetDefault(gname):
          return HttpResponse("Default Gallery For Play Is Set Successfully")
        else:
          return HttpResponse("Gallery %s Not Found"%(gname))
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


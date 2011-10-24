from inc import *
from django.template import Template

def Register(request):
    register_t = loader.get_template('core/_register.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(register_t.render(c))

def ChangePWD(request):
    register_t = loader.get_template('core/_change_pwd.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(register_t.render(c))

def AddService(request):
    form_t = loader.get_template('core/_addservice.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(form_t.render(c))

def ModifyService(request):
    form_t = loader.get_template('core/_mdyservice.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(form_t.render(c))

def AddPost(request,sname):
    form_t = loader.get_template('core/_addpost.html')
    c = Context({"REQUEST":request.REQUEST,"SERVICE":sname})
    return HttpResponse(form_t.render(c))

def AddRoster(request,sname,day):
    form_t = loader.get_template('core/_addroster.html')
    c = Context({"DAY":int(day),"SERVICE":sname})
    return HttpResponse(form_t.render(c))

def ModifyTimeTable(request):
    form_t = loader.get_template('core/_mdytimetable.html')
    c = Context({})
    return HttpResponse(form_t.render(c))


def Login(request):
    login_t = loader.get_template('core/_login.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(login_t.render(c))

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

def AddGallery(request,sname):
    addgallery_t = loader.get_template('core/_addgallery.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(addgallery_t.render(c))

def AddResource(request,sname,respath):
    addgallery_t = None
    if(request.REQUEST.has_key('quick')):
      addgallery_t = loader.get_template('core/image_add_quick.html')
    else:
      addgallery_t = loader.get_template('core/image_add.html')
    c = Context({"SERVICE":sname,"RESPATH":respath})
    return HttpResponse(addgallery_t.render(c))

def ModifyResource(request,sname,respath):
    addgallery_t = None
    if(request.REQUEST.has_key('quick')):
      addgallery_t = loader.get_template('core/image_add_quick.html')
    else:
      addgallery_t = loader.get_template('core/image_add.html')
    c = Context({"SERVICE":sname,"RESPATH":respath,'MODIFY':'STRICT'})
    return HttpResponse(addgallery_t.render(c))

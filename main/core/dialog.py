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

def AddGallery(request,sname):
    addgallery_t = loader.get_template('core/_addgallery.html')
    c = Context({"REQUEST":request.REQUEST})
    return HttpResponse(addgallery_t.render(c))

def ModifyDefaultGallery(request,sname):
    mdy_t = loader.get_template('core/_mdydefaultgallery.html')
    service = GetService(sname)
    if(service):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        gallery = Gallery.InitGalleryConfig(gnode.getroot())
        c = Context({'GALLERYS':json.dumps(gallery.BasicInfo().keys()),'DEFAULT':'None'})
        return HttpResponse(mdy_t.render(c),mimetype="text/html")
    else:
        return HttpResponse("Service %s not exist"%(sname))

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

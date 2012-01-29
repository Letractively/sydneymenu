# Create your views here.
from user import * 
from glue.forum import *
from glue.models import *
from django.core.urlresolvers import reverse
# NOTICE: This is the top level module, do not import this file.

def FBApp(request):
  home_t = loader.get_template('glue/fbapp.html')
  c = Context({'REQUEST':request.REQUEST,'CSS_ROOT':'default','SESSION':request.session})
  return HttpResponse(home_t.render(c))

def FBLogin(request):
  login_t = loader.get_template('glue/fblogin.html')
  c = Context({'SESSION':request.session})
  return HttpResponse(login_t.render(c))

def PersonalCollection(request):
  user = GetUsr(request)
  if (user == "GUEST"):
    return redirect("/glue/login/?next="+reverse("glue.views.PersonalCollection",args=()))
  else:
    user = User.objects.get(username = user)
    collections = ServicesOfUser(user)
    collect_t = loader.get_template('glue/collection.html')
    c = RequestContext(request,{'COLLECTIONS':collections,'SESSION':request.session})
    response = HttpResponse(collect_t.render(c),mimetype = "text/html")
    return response

def Mark(request):
    services = ServiceCore.objects.all()
    mark_t = loader.get_template('glue/mark.html')
    c = RequestContext(request,{'SERVICES':services,'SESSION':request.session})
    response = HttpResponse(mark_t.render(c),mimetype = "text/html")
    return response

def Users(request):
  users_t  = loader.get_template('usrs/allusers.html');
  users = User.objects.all()
  c = RequestContext(request,{'USERS':users,'CSS_ROOT':'default'})
  return HttpResponse(users_t.render(c))


# Create your views here.
from user import * 
from glue.forum import *
# NOTICE: This is the top level module, do not import this file.

def FBApp(request):
  home_t = loader.get_template('glue/fbapp.html')
  c = Context({'REQUEST':request.REQUEST,'CSS_ROOT':'default','SESSION':request.session})
  return HttpResponse(home_t.render(c))

def FBLogin(request):
  login_t = loader.get_template('glue/fblogin.html')
  c = Context({'SESSION':request.session})
  return HttpResponse(login_t.render(c))



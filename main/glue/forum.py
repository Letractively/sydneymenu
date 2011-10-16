from pybb.models import *
from core.user import *
from django.shortcuts import redirect

def AddForum(category,name):
  ckey = Category.objects.get(name = category)
  forum = Forum()
  forum.name = name
  forum.category = ckey
  forum.save()

def DeleteForum(fname):
  try:
    forum = Forum.objects.get(name = fname)
    Forum.delete(forum)
  except:
    pass

def ServiceActivateForum(request,sname):
   command_error = {}
   try:
     forum = Forum.objects.get(name = sname)
     command_error['ERROR'] = "Forum for %s is already exists." % sname
     return GeneralXMLResponse(request,command_error,'Service Forum Already Been Created')
   except Forum.DoesNotExist:
     AddForum('Services',sname);
     return GeneralXMLResponse(request,command_error,'Service Forum Linked Successfully')
   
def ServiceDelForum(request,sname):
   command_error = {}
   DeleteForum(sname)
   return GeneralXMLResponse(request,command_error,'Service Forum Deleted Successfully')

def Login(request):
  command_error = {}
  u_data = {}
  user = request.user
  if user and user.is_authenticated and user.is_active:
    if request.REQUEST.has_key("next"):
      return redirect(request.REQUEST['next'])
    else:
      return redirect("/forum/")
  else:
    command_error = model_obj_builder(u_data,request.REQUEST,login_handler)
    if not command_error:
      user = authenticate(username = u_data['name'],password = u_data['password'])
      if user and user.is_active:
        if request.REQUEST.has_key("next"):
          return redirect(request.REQUEST['next'])
        else:
          return redirect("/forum/")
      else:
        log_t = loader.get_template('usrs/login.html')
        c = Context({'REQUEST':request.REQUEST,'CSS_ROOT':'default'})
        return HttpResponse(log_t.render(c),mimetype = "text/html")
    else:
      log_t = loader.get_template('usrs/login.html')
      c = Context({'REQUEST':request.REQUEST,'CSS_ROOT':'default'})
      return HttpResponse(log_t.render(c),mimetype = "text/html")
 
def Register(request):
  log_t = loader.get_template('usrs/register.html')
  c = Context({'REQUEST':request.REQUEST,'CSS_ROOT':'default'})
  return HttpResponse(log_t.render(c),mimetype = "text/html")

class XMLForum:
  @staticmethod
  def InitForumConfig(node):
    return XMLForum(InitNode(node,"forum","forum"))
  
  def __init__(self,node):
    self.gnode = node

  def IsEnabled(self,sname):
    try:
      forum = Forum.objects.get(name = sname)
      return forum 
    except:
      return None 


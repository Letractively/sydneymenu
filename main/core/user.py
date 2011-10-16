from inc import * 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from hashlib import sha1
import cmd

#Build permission cmd_error
class Permission:
  @staticmethod
  def CreateService(request,sdata,cmd_error):
    if request.user.is_authenticated():
      if request.user.username == 'SYSTEM':
        pass
      elif (request.user.email != sdata.email):
        cmd_error['PERMISSION'] = "EMAIL NOT MATCH"
      else:
        try:
          service_data = ServiceCore.objects.get(email = request.user.email)
          cmd_error['PERMISSION'] = "ACCESS LIMITATION"
        except ServiceCore.DoesNotExist:
          pass
    else:
        cmd_error['PERMISSION'] = "NEED LOGIN"

def GetUsr(request):
  if request.user.is_authenticated():
    return request.user.username
  else:
    return "GUEST"

def HasAuthority(request, s_name):  
  if request.user.is_authenticated():
    u_data = {'name':request.user.username,'email':request.user.email}
    try:
      service_data = ServiceCore.objects.get(name = s_name)
      if (service_data.email == u_data['email'] or u_data['name'] == 'SYSTEM'):
        return {'r':True,'m':'','s':service_data,'u':u_data}
      else:
        return {'r':False,'m':service_data.email+"["+u_data['name']+'|'+u_data['email']+"]"}
    except ServiceCore.DoesNotExist:
      return {'r':False,'m':"Service "+s_name+" does not exists"}
  else:
    return {'r':False,'m':"No login info found"}

def IsSystem(request):
  return (request.user.is_authenticated() and request.user.username == "SYSTEM")

class HistoryHelper:
  @staticmethod
  def Record(request,sname,acttype,para):
    today = date.today()
    now = datetime.now()
    hist = History() 
    hist.type = acttype
    hist.service = sname
    hist.who = GetUsr(request) 
    hist.para = para
    hist.save()
    try:
      service = ServiceCore.objects.get(name = sname)
      service.activity = service.activity + 1
      service.save()
    except ServiceCore.DoesNotExist:
      pass

  @staticmethod
  def GetHistory(sname,acttype,usrname,max):
    hs = History.objects.all().order_by("-id") 
    if(sname):
      hs = hs.filter(service = sname)
    if(acttype):
      hs = hs.filter(type = acttype)
    if(usrname):
      hs = hs.filter(who = usrname)
    if(max):
      hs = hs[:max]
    return hs

def Users(request):
    users = User.objects.all()
    users_t = loader.get_template('usrs/users.html')
    c = Context({"USERS":users})
    return HttpResponse(users_t.render(c),mimetype = "text/html")

def RemoveUser(request,uname):
    command_error = {}
    try:
        user = User.objects.get(username = uname)
        User.delete(user) 
        return GeneralXMLResponse(request,command_error,"User " + uname + " was removed")
    except User.DoesNotExist:
        command_error['MISC'] = 'User ' + uname + ' Does Not Exist'
        return GeneralXMLResponse(request,command_error)


    users = User.objects.all()
    users_t = loader.get_template('usrs/users.html')
    c = Context({"USERS":users})
    return HttpResponse(users_t.render(c),mimetype = "text/html")
    
def Register(request):
    u_data = {}
    command_error = model_obj_builder(u_data,request.REQUEST,reg_handler)
    if command_error:
        register_t = loader.get_template('core/__register_fail.xml')
        c = Context({"ERROR":command_error})
        return HttpResponse(register_t.render(c),mimetype = "text/xml")
    else:
        try:
            user = User.objects.get(email=u_data['email'])
            command_error['ERROR'] = 'email conflict'
            return GeneralXMLResponse(request,command_error,'Email address already been used')
        except User.DoesNotExist:
            try:
              user = User.objects.create_user(u_data['name'],u_data['email'],u_data['password'])
              user.is_active = False
              user.save()
              t = loader.get_template('core/__register_succ.xml')
              c = Context({'CSS_ROOT':'default','REQUEST':request.REQUEST})
              tail = sha1(user.email)
              cmd.SendMail("(zoyoeproject),accout activation",
                     """Thank you for using zoyoeproject, you can use the following link to \
                     activate your account: %s/core/user/activate/%s/%s"""
                     %(request.get_host(),user.username,tail.hexdigest()),
                     user.email) 
              return HttpResponse(t.render(c),mimetype = "text/xml")
            except ValidationError, e:
              command_error['ERROR'] = 'ValidationError';
              register_t = loader.get_template('core/__register_fail.xml')
              return GeneralXMLResponse(request,command_error,e)
            except IntegrityError, e:
              command_error['name'] = 'Name Already Exists';
              command_error['ERROR'] = 'Name Already Exists';
              return GeneralXMLResponse(request,command_error,e)

def ChangePWD(request):
    u_data = {}
    command_error = model_obj_builder(u_data,request.REQUEST,pwd_handler)
    if command_error:
        return GeneralXMLResponse(request,command_error,'Change Password Failed')
    elif request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        user.set_password(u_data['password'])
        user.save()
        return GeneralXMLResponse(request,command_error,'Password Changed Successfully')
    else:
        command_error['ERROR'] = 'Login Required'
        return GeneralXMLResponse(request,command_error,'Login Required')

def Logout(request):
    logout(request)
    return HttpResponse('Logout');

def Activate(request,uname,code):
    command_error = {}
    try:
        user = User.objects.get(username = uname)
        user.is_active = True
        user.save()
        return GeneralXMLResponse(request,command_error)
    except User.DoesNotExist:
        return GeneralXMLResponse(request,command_error)



@session_prefix      
def Login(request):
    command_error = {}
    u_data = {}
    command_error = model_obj_builder(u_data,request.REQUEST,login_handler)
    if command_error:
        return GeneralXMLResponse(request,command_error,'Login Failed: Missing Infomation')
    user = authenticate(username = u_data['name'],password = u_data['password'])
    if user is not None:
        if user.is_active:
            login(request,user)
        else:
            command_error['Validation'] = 'User has not been activated'
    else:
        command_error['Validation'] = 'Invalid Username Or Password'
    login_t = loader.get_template('core/__login.html')
    if command_error:
        return GeneralXMLResponse(request,command_error,'Login Failed')
    else:
        c = Context({'CSS_ROOT':'default','USER_NAME':u_data['name']})
        return HttpResponse(login_t.render(c),mimetype = "text/xml")

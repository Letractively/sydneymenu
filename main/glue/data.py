from glueinc import *
from glue.models import *

def CollectService(request):
   cmd_data = {}
   command_error = {}
   command_error = model_obj_builder(cmd_data,request.REQUEST,collect_handler)
   user = GetUsr(request)
   if command_error: 
     return GeneralXMLResponse(request,command_error)
   if (user == "GUEST"):
     command_error['ERROR'] = "Login Required"
     return GeneralXMLResponse(request,command_error,'Login Required')
   try:
     service = ServiceCore.objects.get(name=cmd_data['name'])
     user = User.objects.get(username = user)
     try:
       collection = CollectInfo.objects.get(service = service,user = user)
       return GeneralXMLResponse(request,command_error,'Service already been collected')
     except CollectInfo.DoesNotExist:
       collect = CreateCollectInfo(service,user)
       collect.save()
       return GeneralXMLResponse(request,command_error,'Service been collected successfully')
   except ServiceCore.DoesNotExist:
     command_error['ERROR'] = "Service " + cmd_data['name'] + " Does Not Exist"
     return GeneralXMLResponse(request,command_error,'Service not exist')

def CollectBy(request):
   cmd_data = {}
   command_error = {}
   command_error = model_obj_builder(cmd_data,request.REQUEST,collect_handler)
   if command_error: 
     return GeneralXMLResponse(request,command_error)
   try:
     service = ServiceCore.objects.get(name = cmd_data['name'])
     return HttpResponse(len(UsersOfService(service)))
   except ServiceCore.DoesNotExist:
     command_error['ERROR'] = "Service Does Not Exist"
     return GeneralXMLResponse(request,command_error,'Service not exist')

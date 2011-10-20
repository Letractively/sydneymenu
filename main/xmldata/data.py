from core import xmlbase
from core.models import *
from core.user import *
from django.template import Template

def Add(request,sname,path):
  aut = HasAuthority(request,sname)
  command_error = {}
  if command_error:
      return GeneralXMLResponse(request,command_error)
  elif (aut['r'] == False):
      command_error['AUTHORITY'] = 'NO_AUTHORITY'
      return GeneralXMLResponse(request,command_error)
  else:
    xsd = aut['s'].extend.GetXSDDoc()
    template_doc = XMLTemplateFromXSD(path,xsd)
    xml_t = Template(str(template_doc))
    c = Context({"REQUEST":request.REQUEST})
    xml_data = xml_t.render(c)
    info = xmlbase.CreateNewInfo(aut['s'],xml_data,path)
    return HttpResponse(info.data,mimetype="text/xml")
    return GeneralXMLResponse(request,command_error)
    
def Remove(request,sname,path):
  return "NotImplemented"

def Modify(request,sname,path):
  return "NotImplemented"


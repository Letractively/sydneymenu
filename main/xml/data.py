from core import xmlbase
from core.models i

def Add(request,sname,path):
  aut = HasAuthority(request,sname)
  command_error = {}
  if command_error:
      return GeneralXMLResponse(request,command_error)
  elif (aut['r'] == False):
      command_error['AUTHORITY'] = 'NO_AUTHORITY'
      return GeneralXMLResponse(request,command_error)
  else:
    xsd = aut['s'].extend.GetXSD()
    template_doc = XMLTemplateFromXSD(path,xsd)
    xml_t = Template(str(template_doc))
    c = Context({"REQUEST":request.REQUEST})
    xml_data = xml_t.render(c)
    xmlbase.CreateNewInfo(aut['s'],xml_data,path)
    return GeneralXMLResponse(request,command_error)
    
def Remove(request,sname,path):
  return "NotImplemented"

def Modify(request,sname,path):
  return "NotImplemented"


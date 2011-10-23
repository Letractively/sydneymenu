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
    return GeneralXMLResponse(request,command_error,"Info has been recorded successfully")
    
def Remove(request,sname,path):
  return "NotImplemented"

def Modify(request,sname,path):
  return "NotImplemented"

def Rend(request,sname,path):
  try:
    service = ServiceCore.objects.get(name=sname)
    db_items = Info.objects.filter(service = sname,path=path)
    ext = service.extend
    attrs = ext.GetXSDDoc().xpath("//xs:complexType[@name='"+path+"']/xs:attribute",
                    namespaces={'xs':'http://www.w3.org/2001/XMLSchema'})
    table_str = "<table class='shortcut'>"
    table_str += "<tr class='title'><td class='btn'></td>"
    for attr in attrs:
      table_str +="<td>"+attr.get("name")+"</td>"
    table_str += "</tr>"
    for item in db_items:
      table_str +="<tr class='datalane' onclick=\"zoyoe.comps['ITEMS'].Select('"+ str(item.id) +"',this)\">"
      table_str +="<td class='btn'><div class='pick'></div></td>"
      for attr in attrs:
        table_str +="<td>"+item.GetDataDoc().getroot().get(attr.get("name"))+"</td>"
      table_str +="</tr>"
    table_str += "</table>"
    return HttpResponse(table_str)
  except ServiceCore.DoesNotExist:
    return HttpResponse("Service is " + sname + " Does Not Exist")

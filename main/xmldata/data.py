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
    xml_t = Template(etree.tostring(template_doc))
    c = Context({"REQUEST":request.REQUEST})
    xml_data = xml_t.render(c)
    info = xmlbase.CreateNewInfo(aut['s'],xml_data,path)
    return GeneralXMLResponse(request,command_error,"Info has been recorded successfully")
    
def Remove(request,sname,id):
  aut = HasAuthority(request,sname)
  command_error = {}
  if command_error:
      return GeneralXMLResponse(request,command_error)
  elif (aut['r'] == False):
      command_error['AUTHORITY'] = 'NO_AUTHORITY'
      return GeneralXMLResponse(request,command_error)
  else:
    try:
      info = Info.objects.get(service=sname,id=id)
      Info.delete(info)
      return GeneralXMLResponse(request,command_error,"Info has been removed successfully")
    except Info.DoesNotExist,e:
      command_error['FAIL'] = "Data Does Not Exist"
      return GeneralXMLResponse(request,command_error)

def Modify(request,sname,path):
  aut = HasAuthority(request,sname)
  tmp = {}
  command_error = {}
  command_error = model_obj_builder(tmp,request.REQUEST,xml_data_handler)
  if command_error:
      return GeneralXMLResponse(request,command_error)
  elif (aut['r'] == False):
      command_error['AUTHORITY'] = 'NO_AUTHORITY'
      return GeneralXMLResponse(request,command_error)
  else:
    try:
      xsd = aut['s'].extend.GetXSDDoc()
      template_doc = XMLTemplateFromXSD(path,xsd)
      xml_t = Template(str(template_doc))
      c = Context({"REQUEST":request.REQUEST})
      xml_data = xml_t.render(c)
      info = xmlbase.ModifyInfo(aut['s'],xml_data,path,request.REQUEST['id'])
      return GeneralXMLResponse(request,command_error,"Info has been recorded successfully")
    except Info.DoesNotExist,e:
      command_error['EXCEPTION'] = 'DATA_NOT_EXIST'
      return GeneralXMLResponse(request,command_error)

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
      table_str +="<tr class='datalane' onclick=\"zoyoe.comps['" + path +"'].Select('"+ str(item.id) +"',this)\">"
      table_str +="<td class='btn'><div class='pick'></div></td>"
      for attr in attrs:
        table_str +="<td>"+item.GetDataDoc().getroot().get(attr.get("name"))+"</td>"
      table_str +="</tr>"
    table_str += "</table>"
    table_str +="<div class='datalane' onclick=\"zoyoe.comps['" + path + "'].Select(-1,this)\">Append Data </div>"
    return HttpResponse(table_str)
  except ServiceCore.DoesNotExist:
    return HttpResponse("Service is " + sname + " Does Not Exist")

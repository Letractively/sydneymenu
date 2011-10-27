from core.inc import *
from django.template import Template

def XSDDialog(request,sname,path):
    s_data = GetService(sname) 
    if(s_data == None):
      return HttpResponse('Service Not Exist')
    else:
      item = None
      if(request.REQUEST.has_key('id')):
          db_item = Info.objects.get(id = int(request.REQUEST['id']))
          item = db_item.GetDataDoc()
      s_xsd = s_data.extend.GetXSDDoc()
      form_t = Template("{% load comp_filters %}\n" +
        "{%load hash_filters %}\n" +
        etree.tostring(FormFromXSD(path,s_xsd)))
      c = Context({"ITEM":item,"PATH":path})
      return HttpResponse(form_t.render(c),mimetype="text")

from core.user import * 
from django.template import Context, loader, RequestContext
def Main(request,sname,path):
   try:
      service = ServiceCore.objects.get(name=sname) 
      gallery_t = loader.get_template('gallery/main.html')
      c = RequestContext (request,{'SERVICE':service})
      response = HttpResponse(gallery_t.render(c),mimetype = "text/html")
      return response
   except ServiceCore.DoesNotExist:
      return HttpResponse("Service Does Not Exist")
    


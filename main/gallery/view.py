from core.user import * 
from django.template import Context, loader, RequestContext
def View(request,sname,path):
   try:
      service = ServiceCore.objects.get(name=sname) 
      gallery_t = loader.get_template('gallery/gallery.html')
      c = RequestContext (request,{'SERVICE':service})
      response = HttpResponse(gallery_t.render(c),mimetype = "text/html")
      return response
   except ServiceCore.DoesNotExist:
      return HttpResponse("Service Does Not Exist")
    
def Main(request):
   items = core.Info.objects.all[:12]
   gallery_t = loader.get_template('gallery/main.html')
   c = RequestContext (request,{'ITEMS':items})
   response = HttpResponse(gallery_t.render(c),mimetype = "text/html")
   return response
 

# Create your views here.
from user import * 
from glue.forum import *
from django.db.models import Q
from garden.models import *
from garden.mesh import *

@browser_prefix
def Main(request):
    today = date.today()
    now = datetime.now()
    tstamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    dic = {}
    user = GetUsr(request)
    if (user == "GUEST"):
      return redirect("/glue/login/?next="+reverse("garden.views.Main",args=()))
    if (not (user.startswith("fb_"))):
      return HttpResponse("You need login with your facebook account to using this fb application")
    garden = GetGardenOption(request.user)
    if(garden == None):
      garden = CreateGarden(request.user)
    name = garden.entity.name
    gnode = GetConfigDoc(garden.entity)
    layout = Layout.InitLayoutConfig(gnode.getroot())
    gallery = Gallery.InitGalleryConfig(gnode.getroot())
    gallery_info = gallery.BasicInfo()
    garden_t = loader.get_template('garden/main.html')
    dic['SERVICE'] = garden
    dic['ROOT'] = True 
    dic['COMP'] = garden.entity.BuildComp()
    dic['GALLERY_INFO'] = gallery_info
    dic['SESSION'] = request.session
    dic['CSS_COLOR'] = layout.GetColor() 
    dic['WEATHER'] = GetWeatherInfo()
    dic['HAS_AUTHORITY'] = True 
    c = RequestContext(request,dic)
    return HttpResponse(garden_t.render(c),mimetype = "text/html")

@browser_prefix
def Sensis(request,gear,plant): 
    results = GetSensisServiceList(gear,plant)
    sensis_t = loader.get_template('garden/sensis.html')
    dic = {}
    dic['SENSIS'] = results
    dic['CSS_COLOR'] = ['white','steelblue','steelblue','ghostwhite']
    c = RequestContext(request,dic)
    return HttpResponse(sensis_t.render(c),mimetype = "text/html")

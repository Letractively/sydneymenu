# Create your views here.
from user import * 
from glue.forum import *
import glue
from django.db.models import Q
from garden.models import *
from garden.mesh import *

def DecodeBase64Url(token):
    padding_factor = (4 - len(token) % 4) % 4
    token += "="*padding_factor
    return base64.b64decode(unicode(token).translate(dict(zip(map(ord,
u'-_'), u'+/'))))

@browser_prefix
def FBApp(request):
    sig,payload = request.REQUEST['signed_request'].split('.',2)
    sig = DecodeBase64Url(sig)
    data = json.loads(DecodeBase64Url(payload))
    user_id = data.get('user_id')
    token = data.get('oauth_token')
    user = glue.middleware.LoginFBUser(request,user_id,token)
    if(user):
      return redirect(reverse("garden.views.Main",args=()))
    else:
      return redirect("/glue/login/?next="+reverse("garden.views.Main",args=()))

@browser_prefix
def Main(request):
    today = date.today()
    now = datetime.now()
    tstamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    dic = {}
    user = GetUsr(request)
    if (user == None):
      return redirect("/glue/login/?next="+reverse("garden.views.Main",args=()))
    garden = GetGardenOption(request.user)
    if(garden == None):
      garden = CreateGarden(request.user)
    name = garden.entity.name
    garden_t = loader.get_template('garden/main.html')
    config = GetConfig(garden.entity)
    dic['SERVICE'] = garden
    dic['ROOT'] = True 
    dic['COMP'] = garden.entity.BuildComp()
    dic['SESSION'] = request.session
    dic['CSS_COLOR'] = config['layout']['color'] 
    dic['WEATHER'] = GetWeatherInfo()
    dic['HAS_AUTHORITY'] = True 
    dic['CONFIG'] = config 
    c = RequestContext(request,dic)
    return HttpResponse(garden_t.render(c),mimetype = "text/html")

@browser_prefix
def SinglePlant(request,pname):
    today = date.today()
    now = datetime.now()
    tstamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    dic = {}
    user = GetUsr(request)
    if (user == 'SYSTEM'):
      dic['HAS_AUTHORITY'] = True
    else:
      dic['HAS_AUTHORITY'] = False 
    formal_name = GetFormalName(pname)
    plant = GetPlantOption(formal_name)
    if(plant == None):
      if (request.REQUEST.has_key('create')):
        plant = CreatePlant(formal_name)
    if(plant == None):
      return HttpResponse('plant not found') 
    name = plant.entity.name
    plant_t = loader.get_template('garden/plant.html')
    config = GetConfig(plant.entity)
    dic['SERVICE'] = plant 
    dic['ROOT'] = True 
    dic['COMP'] = plant.entity.BuildComp()
    dic['SESSION'] = request.session
    dic['CSS_COLOR'] = config['layout']['color'] 
    dic['CONFIG'] = config 
    c = RequestContext(request,dic)
    return HttpResponse(plant_t.render(c),mimetype = "text/html")

@browser_prefix
def Plants(request):
    plants_t = loader.get_template('garden/plants.html')
    plants = Plant.objects.all()
    c = RequestContext(request,{'PLANTS':plants})
    return HttpResponse(plants_t.render(c),mimetype = "text/html")

@browser_prefix
def Sensis(request,gear,plant): 
    results = GetSensisServiceList(gear,plant)
    sensis_t = loader.get_template('garden/sensis.html')
    dic = {}
    dic['SENSIS'] = results 
    dic['SENSIS_PATH'] = gear + "/" + plant 
    dic['CSS_COLOR'] = ['white','steelblue','steelblue','ghostwhite']
    c = RequestContext(request,dic)
    return HttpResponse(sensis_t.render(c),mimetype = "text/html")

@browser_prefix
def SensisJSON(request,gear,plant): 
    results = GetSensisServiceListString(gear,plant)
    return HttpResponse("var sensis_obj = " + results,mimetype = "text/javascript")


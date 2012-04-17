# Create your views here.
from user import * 
from glue.forum import *
from django.db.models import Q
from garden.models import *
from garden.mesh import *

def Config(request):
  PLANT_ICON_LIST = [{'name':'vegetable','imgs':[]},{'name':'flower','imgs':[]}]
  PLANT_ICON_LIST[0]['imgs'].append({'name':'test','url':'/res/res_error.png'})
  PLANT_ICON_LIST[0]['imgs'].append({'name':'amaranth','url':'/garden/gallery/image/amaranth.jpg'})
  GINFO = {'backend':'internal','albums':PLANT_ICON_LIST}
  return HttpResponse(json.dumps(GINFO))

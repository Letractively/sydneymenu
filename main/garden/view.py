# Create your views here.
from user import * 
from glue.forum import *
from search import *
from django.db.models import Q

@browser_prefix
def Main(request):
    today = date.today()
    now = datetime.now()
    tstamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    dic = {}
    user = GetUsr(request)
    if (user == "GUEST"):
      return redirect("/glue/login/?next="+reverse("garden.views.Main",args=()))
    entity = GetGardenEntityOption(request.user)
    if(entity == None):
      entity = CreateGardenEntity(request.user)
    name = entity.name
    gnode = etree.parse(CONFIG.GARDEN_PATH + name+'/config.xml')
    layout = Layout.InitLayoutConfig(gnode.getroot())
    gallery = Gallery.InitGalleryConfig(gnode.getroot())
    forum_info = XMLForum.InitForumConfig(layout.RightNode())
    gallery_info = gallery.BasicInfo()
    layout_info = layout.GetLayout()
    photo_info = PhotoPlay.InitPhotoPlayConfig(gnode.getroot()).BasicInfo()
    template = layout.GetTemplate()
    color = layout.GetColor()
    dic['CSS_ROOT'] = template 
    dic['CSS_COLOR'] = color 
    garden_t = loader.get_template('garden/create.html')
    dic['ENTITY'] = data
    dic['COMP'] = data.entity.BuildComp()
    dic['GALLERY_INFO'] = gallery_info
    dic['PHOTO_INFO'] = photo_info
    dic['HIST'] = HistoryHelper.GetHistory(name,None,None,10) 
    dic['SESSION'] = request.session
    c = RequestContext(request,dic)
    return HttpResponse(garden_t.render(c),mimetype = "text/html")

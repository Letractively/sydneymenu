# Create your views here.
from user import * 
from glue.forum import *
# NOTICE: This is the top level module, do not import this file.

def ShortCut(request,name):
    service_t = loader.get_template('core/shortcut.html')
    try:
      data = ServiceCore.objects.get(name=name)
      c = Context({'REQUEST':request.REQUEST,'DATA':data})
      return HttpResponse(service_t.render(c),mimetype = "text/xml")
    except ServiceCore.DoesNotExist:
      return HttpResponse("Error")

def Admin(request):
# The get service will always provides all the services
    services = ServiceCore.objects.all()
    data_t = loader.get_template('core/admin.html')
    c = Context({'DATA':services,'SESSION':request.session})
    response = HttpResponse(data_t.render(c),mimetype = "text/html")
    response['Cache-Control'] = 'no-cache'
    return response

def List(request):
    filter_str = request.REQUEST['filter']
    filter_dict = json.loads(filter_str)
    services = ServiceCore.objects.all();
    if(filter_dict.has_key('NATION') and filter_dict['NATION'] != 'MIXED'):
      nations = filter_dict['NATION'].split(',')
      nations.append("MIXED")
      regex = "|".join(nations);
      services = services.filter(nation__regex=regex)
    if(filter_dict.has_key('STYPE')):
      types = filter_dict['STYPE'].split(',')
      regex = "|".join(types);
      services = services.filter(type__regex=regex)
    if(filter_dict.has_key('PRICE') 
      and filter_dict['PRICE'].has_key('MAX')): 
      services = services.filter(pricelow__lte = (int (filter_dict['PRICE']['MAX'])))
    results = []
    distances = {}
    if(filter_dict.has_key('LOCATION') and filter_dict.has_key('RADIUS')):
      llbase = {'lat':float(filter_dict['LOCATION']['x']),'long':float(filter_dict['LOCATION']['y'])}
      if llbase['lat'] and llbase['long'] and filter_dict['RADIUS']:
        for service in services:
          llinc = {'lat':float(service.latitude)/1000000,'long':float(service.longitude)/1000000}
          dis = ComputeDistance(llbase,llinc)
          if(dis < int(filter_dict['RADIUS'])):
            distances[service.name] = dis
            results.append(service)
      else:
        for service in services:
          results.append(service)
    else:
      for service in services:
        results.append(services)
    data_t = loader.get_template('core/admin.html')
    loc = filter_dict['LOCATION']
    c = RequestContext(request,{'DATA':results,"LOC":loc,"DIS":distances})
    response = HttpResponse(data_t.render(c),mimetype = "text/html")
    response['Cache-Control'] = 'no-cache'
    return response

def Service(request,name):
    comp_dict = {'news':'comp/_news.html',
                 'icon':'comp/_icon.html',
                 'gallery':'comp/_gallery.html',
                 'items':'comp/_items.html',
                 'photo-player':'comp/_photos.html',
                 'timetable':'comp/_timetable.html',
                 'roster':'comp/_roster.html'}
    aut = HasAuthority(request,name)
    service_t = None
    today = date.today()
    now = datetime.now()
    tstamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    dic = {'CSS_ROOT':'default'}
    if (request.REQUEST.has_key('comp') and comp_dict.has_key(request.REQUEST['comp'])):
      comp = request.REQUEST['comp']
      service_t = loader.get_template(comp_dict[comp])
      if (request.REQUEST.has_key('day')):
        dic['WEEK_DAY'] = CONFIG.WEEK_DAY_NAME[int (request.REQUEST['day'])]
      else:
        dic['WEEK_DAY'] = CONFIG.WEEK_DAY_NAME[today.weekday()]
    else:
      service_t = loader.get_template('core/service.html')
      dic['ROOT'] = 'ROOT'
      dic['WEEK_DAY'] = CONFIG.WEEK_DAY_NAME[today.weekday()]
    try:
      data = ServiceCore.objects.get(name=name)
      dic['SERVICE'] = data
      dic['COMP'] = data.BuildComp()
      if (aut['r'] == True):
        dic['HAS_AUTHORITY'] = True
        dic['TIME_STAMP'] = tstamp
      gnode = etree.parse(CONFIG.SERVICES_PATH + name+'/config.xml')
      layout = Layout.InitLayoutConfig(gnode.getroot())
      gallery = Gallery.InitGalleryConfig(gnode.getroot())
      forum_info = XMLForum.InitForumConfig(layout.RightNode())
      gallery_info = gallery.BasicInfo()
      layout_info = layout.GetLayout()
      photo_info = PhotoPlay.InitPhotoPlayConfig(gnode.getroot()).BasicInfo()
      dic['GALLERY_INFO'] = gallery_info
      dic['PHOTO_INFO'] = photo_info
      dic['ROSTER_INFO'] = {}
      dic['LAYOUT_INFO'] = layout_info
      dic['FORUM'] = forum_info.IsEnabled(name)
      dic['HIST'] = HistoryHelper.GetHistory(name,None,None,10) 
      dic['SESSION'] = request.session
      c = RequestContext(request,dic)
      return HttpResponse(service_t.render(c),mimetype = "text/html")
    except ServiceCore.DoesNotExist:
      return HttpResponse("Service Does Not Exist")

def Map(request):
  home_t = loader.get_template('core/map.html')
  hist = HistoryHelper.GetHistory(None,None,None,10)
  c = RequestContext(request,{'REQUEST':request.REQUEST,'CSS_ROOT':'default','HIST':hist,'SESSION':request.session})
  return HttpResponse(home_t.render(c))

def Search(request):
  home_t = loader.get_template('core/search.html')
  c = Context({'REQUEST':request.REQUEST,'CSS_ROOT':'default','SESSION':request.session})
  return HttpResponse(home_t.render(c))

from user import *
#NOTICE: This is the top level module, do not import this file

def SetRange(request,sname,day):
    command_error = {}
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
      command_error['AUTHORITY'] = 'NO_AUTHORITY'
      return GeneralXMLResponse(request,command_error)
    data = aut['s'] 
    rs = {}
    command_error = model_obj_builder(rs,request.REQUEST,set_timerange_handler)
    if command_error:
      return GeneralXMLResponse(request,command_error,'Invalid Input')
    else:
      if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        ttable = TimeTable.InitTimeTableConfig(gnode.getroot())
        int_reg = re.compile('(\d+)')
        e = int(int_reg.search(rs['start']).group(1))
        l = int(int_reg.search(rs['end']).group(1))
        if (e >= 24):
          ttable.SetRange(int(day),0,0)
        elif (l >= 24):
          ttable.SetRange(int(day),rs['start'],'24:00')
        else:
          ttable.SetRange(int(day),rs['start'],rs['end'])
        SaveConfig(sname,gnode)
        return GeneralXMLResponse(request,command_error,'Time Range was Set Successfully')
      else:
        command_error['MISC'] = 'Service Not Activated'
        return GeneralXMLResponse(request,command_error)

def AddSlot(request,sname,day,slot):
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        return HttpResponse(aut['m'])
    if (request.REQUEST.has_key('info')):
      data = ServiceCore.objects.get(name = sname)
      if (data.activate == True):
        fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_RDWR)
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        ttable = TimeTable.InitTimeTableConfig(gnode.getroot())
        if (ttable.RequireSlot(day,slot,request.REQUEST['info']) != None):
          fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_RDWR)
          os.write(fd,etree.tostring(gnode,pretty_print = True))
          os.close(fd)
          return HttpResponse("Slot Created")
        else:
          return HttpResponse("Slot Not Created")
      else:
        return HttpResponse("Service Not Activated") 
    else:
      return HttpResponse("Slot Info Required")

def DelSlot(request,sname,day,slot):
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        return HttpResponse(aut['m'])
    data = ServiceCore.objects.get(name = sname)
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        ttable = TimeTable.InitTimeTableConfig(gnode.getroot())
        if (ttable.ClearSlot(day,slot) != None):
          fd = os.open(CONFIG.SERVICES_PATH + sname+'/config.xml',os.O_RDWR)
          os.write(fd,etree.tostring(gnode,pretty_print = True))
          os.close(fd)
          return HttpResponse("Slot Deleted")
        else:
          return HttpResponse("Slot Not Deleted")
    else:
        return HttpResponse("Service Not Activated") 


from user import *
#NOTICE: This is the top level module, do not import this file

def Add(request,sname,day):
    command_error = {}
    rost_attr = {}
    command_error = model_obj_builder(rost_attr,request.REQUEST,addroster_handler)
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = aut['s']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        ttable = TimeTable.InitTimeTableConfig(gnode.getroot())
        if (ttable.AddRoster(int(day),rost_attr['name']) != None):
          SaveConfig(sname,gnode)
          return GeneralXMLResponse(request,command_error,"Girl Add Successfully, Press Ok To Refresh The Page!!")
        else:
          command_error['MISC'] = "COMMAND FAIL,REASON UNKNOW"
          return GeneralXMLResponse(request,command_error)
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error)

def Remove(request,sname,day):
    command_error = {}
    rost_attr = {}
    command_error = model_obj_builder(rost_attr,request.REQUEST,delroster_handler)
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = aut['s']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        ttable = TimeTable.InitTimeTableConfig(gnode.getroot())
        if (ttable.RemoveRoster(int(day),rost_attr['name']) != None):
          SaveConfig(sname,gnode)
          return GeneralXMLResponse(request,command_error,"Roster Removed Successfully, Press Ok To Refresh The Page!!")
        else:
          command_error['MISC'] = "COMMAND FAIL,REASON UNKNOW"
          return GeneralXMLResponse(request,command_error)
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error)



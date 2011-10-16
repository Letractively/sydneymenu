from user import *
#NOTICE: This is the top level module, do not import this file

def Add(request,sname):
    command_error = {}
    item_attr = {}
    command_error = model_obj_builder(item_attr,request.REQUEST,additem_handler)
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = item_attr['data']
    category = item_attr['category']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        girls = Girls.InitGirlsConfig(gnode.getroot())
        if (girls.AddGirl(girl_attr['name'],girl_attr,desc) != None):
          SaveConfig(sname,gnode)
          HistoryHelper.Record(request,aut['s'].name,"ITEM_ADD",girl_attr['name'])
          return GeneralXMLResponse(request,command_error,"ITEM Add Successfully, Press Ok To Refresh The Page!!")
        else:
          command_error['MISC'] = "COMMAND FAIL,REASON UNKNOW"
          return GeneralXMLResponse(request,command_error)
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error)

def Remove(request,sname,gname):
    aut = HasAuthority(request,sname)
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error,'You Have No Authority To Do This.')
    data = aut['s']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        girls = Girls.InitGirlsConfig(gnode.getroot())
        girls.RemoveGirl(gname)
        SaveConfig(sname,gnode)
        HistoryHelper.Record(request,aut['s'].name,"ITEM_REMOVE",gname)
        return GeneralXMLResponse(request,command_error,"ITEM " +gname +"  Delete Successfully")
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error,'Service' + sname + ' Not Activated')


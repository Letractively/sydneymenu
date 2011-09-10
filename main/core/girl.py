from user import *
#NOTICE: This is the top level module, do not import this file

def Add(request,sname):
    command_error = {}
    girl_attr = {}
    command_error = model_obj_builder(girl_attr,request.REQUEST,addgirl_handler)
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = aut['s']
    desc = girl_attr['description']
    del girl_attr['description']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        girls = Girls.InitGirlsConfig(gnode.getroot())
        if (girls.AddGirl(girl_attr['name'],girl_attr,desc) != None):
          SaveConfig(sname,gnode)
          HistoryHelper.Record(request,aut['s'].name,"GIRL_ADD",girl_attr['name'])
          return GeneralXMLResponse(request,command_error,"Girl Add Successfully, Press Ok To Refresh The Page!!")
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
        HistoryHelper.Record(request,aut['s'].name,"GIRL_REMOVE",gname)
        return GeneralXMLResponse(request,command_error,"Girl " +gname +"  Delete Successfully")
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error,'Service' + sname + ' Not Activated')


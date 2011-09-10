from user import *
#NOTICE: This is the top level module, do not import this file

def Save(request,sname):
    aut = HasAuthority(request,sname)
    temp_dict = {}
    command_error = model_obj_builder(temp_dict,request.REQUEST,savelayout_handler)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = aut['s']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        layout = Layout.InitLayoutConfig(gnode.getroot())
        layout.SaveLayout(temp_dict)
        SaveConfig(sname,gnode)
        return GeneralXMLResponse(request,command_error,"Layout Saved")
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error)


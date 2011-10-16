from user import *
#NOTICE: This is the top level module, do not import this file

def Add(request,sname):
    command_error = {}
    post_attr = {}
    command_error = model_obj_builder(post_attr,request.REQUEST,addpost_handler)
    aut = HasAuthority(request,sname)
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error)
    if (command_error):
        return GeneralXMLResponse(request,command_error)
    data = aut['s']
    post_data = request.REQUEST['post']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        post = Post.InitPostConfig(gnode.getroot())
        if (post.AddPost(post_attr['name'],str(date.today().isoformat())) != None):
#Should Abstract the following into a function
          fd = os.open(CONFIG.SERVICES_PATH + sname+'/'+post_attr['name'] + '.post',os.O_CREAT|os.O_WRONLY)
          os.write(fd,post_data)
          os.close(fd)
          SaveConfig(sname,gnode)
          HistoryHelper.Record(request,aut['s'].name,"POST_ADD",post_attr['name'])
          return GeneralXMLResponse(request,command_error,"Post Add Successfully, Press Ok To Refresh The Page!!")
        else:
          command_error['MISC'] = "COMMAND FAIL,REASON UNKNOW"
          return GeneralXMLResponse(request,command_error)
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error)

def Remove(request,sname,pname):
    aut = HasAuthority(request,sname)
    command_error = {}
    if (aut['r'] == False):
        command_error['AUTHORITY'] = 'NO_AUTHORITY'
        return GeneralXMLResponse(request,command_error,'You Have No Authority To Do This.')
    data = aut['s']
    if (data.activate == True):
        gnode = etree.parse(CONFIG.SERVICES_PATH + sname+'/config.xml')
        post = Post.InitPostConfig(gnode.getroot())
        post.RemovePost(pname)
        fd = os.remove(CONFIG.SERVICES_PATH + sname+'/'+pname + '.post')
        SaveConfig(sname,gnode)
        HistoryHelper.Record(request,aut['s'].name,"POST_REMOVE",pname)
        return GeneralXMLResponse(request,command_error,"Post " +pname +"  Delete Successfully")
    else:
        command_error['MISC'] = "SERVICE NOT ACTIVATED"
        return GeneralXMLResponse(request,command_error,'Service' + sname + ' Not Activated')


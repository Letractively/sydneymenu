# This File is used to update init.config for all the services form version null to version 1.0
import os, sys
path = os.path.join(os.path.abspath('..'), 'adult')
print path
sys.path.append(os.path.join(os.path.abspath('..'), 'adult'))


#print sys.path
print "-----------------"
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


from core.user import *
from core.models import ServiceRel 
from pybb.models import Forum,Category

def Patch(serv):
    gnode = etree.parse(CONFIG.SERVICES_PATH + serv.name+'/config.xml')
    layout = Layout.InitLayoutConfig(gnode.getroot())
    mid_node = layout.MidNode()
    post_node = InitNode(layout.MidNode(),"post_list","post_list")
    mid_node.remove(post_node)
    news_node = InitNode(layout.MidNode(),"news","news")
    SaveConfig(serv.name,gnode)
    

services = ServiceCore.objects.all()
for serv in services:
    Patch(serv)
    print "Patching Service ... " + serv.name
 
print 'Patch Has Been Applied'


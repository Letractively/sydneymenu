from django.conf.urls.defaults import *
from settings import ROOT
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#(r'^test/','test.Test'),

urlpatterns = patterns('',
    (r'^google2cc4d0d43e33a613.html$','glue.views.Verify'),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/res/icons/zoyoe.jpg'}),
    (r'^/{0,1}$','main.glue.views.StartUsing'),
    (r'^zoyoe/$','main.glue.views.StartUsing'),
    (r'^zoyoe/mission/$','main.glue.views.Mission'),
    (r'^zoyoe/startusing/$','main.glue.views.StartUsing'),
    (r'^zoyoe/program/$','main.glue.views.Program'),
    (r'^zoyoe/support/$','main.glue.views.Support'),
    (r'^glue/',include('main.glue.urls')),
    (r'^accounts/',include('main.glue.urls')),
    (r'^map/','main.core.views.Map'),
    (r'^log/','main.core.log.index'),
    (r'^mark/','main.glue.views.Mark'),
#   (r'^search/','main.core.views.Search'),
    (r'^fbapp/','main.glue.views.FBApp'),
    (r'^core/', include('main.core.urls')),
    (r'^gallery/', include('main.gallery.urls')),
    (r'^xml/', include('main.xmldata.urls')),
    (r'^forum/',include('main.pybb.urls')),
# garden facebook application
    (r'^garden/',include('main.garden.urls')),
# following are none stable stuff
    (r'^game/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'game/run/'}),
    (r'^wiki/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'wiki/'}),
    (r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'css'}),
    (r'^res/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'res'}),
    (r'^services/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'services'}),
    (r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'js'}),
    (r'^ckeditor/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'ckeditor'})
)

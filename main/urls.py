from django.conf.urls.defaults import *
from settings import ROOT
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
#(r'^test/','test.Test'),

urlpatterns = patterns('',
    (r'^/{0,1}$','main.core.views.Main'),
    (r'^zoyoe/$','main.core.views.Main'),
    (r'^map/','main.core.views.Map'),
    (r'^mark/','main.core.views.Mark'),
    (r'^log/','main.core.log.index'),
    (r'^search/','main.core.views.Search'),
    (r'^fbapp/','main.glue.views.FBApp'),
    (r'^core/', include('main.core.urls')),
    (r'^gallery/', include('main.gallery.urls')),
    (r'^xml/', include('main.xmldata.urls')),
    (r'^forum/',include('main.pybb.urls')),
    (r'^glue/',include('main.glue.urls')),
    (r'^accounts/',include('main.glue.urls')),
    (r'^game/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'game/run/'}),
    (r'^wiki/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'wiki/'}),
    (r'^css/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'css'}),
    (r'^res/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'res'}),
    (r'^services/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'services'}),
    (r'^js/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'js'}),
    (r'^ckeditor/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'ckeditor'})
    # Example:
    # (r'^sdist/', include('sdist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

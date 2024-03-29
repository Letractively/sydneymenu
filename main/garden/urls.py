from django.conf.urls.defaults import *
from settings import ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^main/$','garden.views.Main'),
    (r'^fbapp/$','garden.views.Main'),
    (r'^plant/(?P<pname>[^/]*)/$','garden.views.SinglePlant'),
    (r'^allplants/$','garden.views.Plants'),
    (r'^plants/$','garden.data.Plants'),
    (r'^hint/(?P<gear>[^/]*)/(?P<plant>[^/]*)/$', 'garden.views.Sensis'),
    (r'^gallery/config/$','garden.data.Config'),
    (r'^sensis/(?P<gear>[^/]*)/(?P<plant>[^/]*)/$', 'garden.views.SensisJSON'),
    (r'^gallery/image/(?P<path>.*)$','django.views.static.serve',{'document_root':ROOT + 'garden/res/'}),
)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^main/$','garden.views.Main'),
    (r'^hint/(?P<gear>[^/]*)/(?P<plant>[^/]*)/$', 'garden.views.Sensis'),
)

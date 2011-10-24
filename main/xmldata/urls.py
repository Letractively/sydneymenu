from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^dialog/xsd/(?P<sname>[^/]*)/(?P<path>.*)/$','xmldata.dialog.XSDDialog'),
    (r'^add/(?P<sname>[^/]*)/(?P<path>.*)/$','xmldata.data.Add'),
    (r'^modify/(?P<sname>[^/]*)/(?P<path>.*)/$','xmldata.data.Modify'),
    (r'^remove/(?P<sname>[^/]*)/(?P<id>.*)/$','xmldata.data.Remove'),
    (r'^rend/(?P<sname>[^/]*)/(?P<path>.*)/$','xmldata.data.Rend'),
    # Example:
    # (r'^sdist/', include('sdist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
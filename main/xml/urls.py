from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^add/(?P<sname>[^/]*)/(?P<path>.*)/$','xml.data.Add'),
    (r'^modify/(?P<sname>[^/]*)/(?P<path>.*)/$','core.data.Modify'),
    (r'^remove/(?P<sname>[^/]*)/(?P<path>.*)/$','core.data.Remove'),
    # Example:
    # (r'^sdist/', include('sdist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

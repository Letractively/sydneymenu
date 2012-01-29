from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^forum-activate/(?P<sname>.*)/$','glue.forum.ServiceActivateForum'),
    (r'^forum-delete/(?P<sname>.*)/$','glue.forum.ServiceDelForum'),
    (r'^login/$','glue.forum.Login'),
    (r'^register/$','glue.forum.Register'),
    (r'^collect/$','glue.data.CollectService'),
    (r'^collectby/$','glue.data.CollectBy'),
    (r'^fblogin/$','glue.views.FBLogin'),
    (r'^users/$','glue.views.Users'),
    (r'^collection/personal/$','glue.views.PersonalCollection'),
    # Example:
    # (r'^sdist/', include('sdist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

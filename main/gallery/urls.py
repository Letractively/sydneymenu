from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^view/(?P<sname>[^/]*)/(?P<path>[a-zA-Z0-9/]*)/$','gallery.view.Main'),
    (r'^info/(?P<sname>[^/]*)/$','gallery.data.GalleryInfo'),
    (r'^add/(?P<sname>[^/]*)/$','gallery.data.Add'),
    (r'^remove/(?P<sname>[^/]*)/(?P<gname>.*)/$','gallery.data.Remove'),
    (r'^imagecache/(?P<sname>.*)/(?P<method>.*)/$','gallery.data.ImageCache'),
    (r'^imagelink/(?P<sname>[^/]*)/(?P<respath>[a-zA-Z0-9/]*)/$','gallery.data.ImageLink'),
    (r'^image/(?P<sname>[^/]*)/(?P<res>.*)/$','gallery.data.Resource'),
)

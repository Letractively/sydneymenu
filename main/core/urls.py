from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/$','core.views.Admin'),
    (r'^services/$','core.views.List'),
    (r'^data/addreport/$','core.data.Report'),
    (r'^data/addservice/$','core.data.AddService'),
    (r'^data/mdyservice/(?P<sname>[^/]*)/$','core.data.ModifyService'),
    (r'^data/delservice/(?P<sname>[^/]*)/$','core.data.RemoveService'),
    (r'^data/getservices/$','core.data.GetServices'),
    (r'^data/activate/(?P<name>.*)/$','core.data.ActivateService'),
    (r'^data/reset/(?P<name>.*)/$','core.data.ResetService'),
    (r'^data/res/(?P<sname>[^/]*)/(?P<res>.*)/$','core.data.Resource'),
    (r'^user/register/$','core.user.Register'),
    (r'^user/login/$','core.user.Login'),
    (r'^user/logout/$','core.user.Logout'),
    (r'^user/users/$','core.user.Users'),
    (r'^user/changepwd/$','core.user.ChangePWD'),
    (r'^user/remove/(?P<uname>.*)/$','core.user.RemoveUser'),
    (r'^user/activate/(?P<uname>[^/]*)/(?P<code>[^/]*)/$','core.user.Activate'),
    (r'^dialog/addservice/$','core.dialog.AddService'),
    (r'^dialog/mdyservice/$','core.dialog.ModifyService'),
    (r'^dialog/mdytimetable/$','core.dialog.ModifyTimeTable'),
    (r'^dialog/xsd/(?P<sname>[^/]*)/(?P<path>.*)/$','core.dialog.XSDDialog'),
    (r'^dialog/addpost/(?P<sname>.*)/$','core.dialog.AddPost'),
    (r'^dialog/addroster/(?P<sname>.*)/(?P<day>[\d])/$','core.dialog.AddRoster'),
    (r'^dialog/register/$','core.dialog.Register'),
    (r'^dialog/changepwd/$','core.dialog.ChangePWD'),
    (r'^dialog/login/$','core.dialog.Login'),
    (r'^dialog/(?P<sname>[^/]*)/gallery/$','core.dialog.GetGallery'),
    (r'^dialog/addgallery/(?P<sname>[^/]*)/$','core.dialog.AddGallery'),
    (r'^dialog/addres/(?P<sname>[^/]*)/(?P<respath>.*)/$','core.dialog.AddResource'),
    (r'^dialog/modifyres/(?P<sname>[^/]*)/(?P<respath>.*)/$','core.dialog.ModifyResource'),
    (r'^gallery/(?P<sname>[^/]*)/add/$','core.gallery.Add'),
    (r'^gallery/(?P<sname>[^/]*)/remove/(?P<gname>.*)/$','core.gallery.Remove'),
    (r'^roster/(?P<sname>[^/]*)/add/(?P<day>[\d])/$','core.roster.Add'),
    (r'^roster/(?P<sname>[^/]*)/remove/(?P<day>[\d])/$','core.roster.Remove'),
    (r'^post/(?P<sname>[^/]*)/add/$','core.post.Add'),
    (r'^post/(?P<sname>[^/]*)/remove/(?P<pname>[^/].*)/$','core.post.Remove'),
    (r'^layout/(?P<sname>[^/]*)/save/$','core.layout.Save'),
    (r'^shortcut/(?P<name>.*)/$','core.views.ShortCut'),
    (r'^service/(?P<name>.*)/$','core.views.Service'),
    (r'^imagecache/(?P<sname>.*)/(?P<method>.*)/$','core.data.ImageCache'),
    (r'^imagelink/(?P<sname>[^/]*)/(?P<rname>.*)/$','core.data.ImageLink'),
    (r'^imageadd/(?P<sname>[^/]*)/(?P<rname>.*)/$','core.data.ImageAdd'),
    (r'^timetable/(?P<sname>.*)/(?P<day>[\d])/','core.timetable.SetRange'),
    # Example:
    # (r'^sdist/', include('sdist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

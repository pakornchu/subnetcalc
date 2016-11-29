from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ip.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'web.views.showIndex'),
    url(r'^ipv4check/$', 'web.views.checkIP4'),
    url(r'^ipv4/$', 'web.views.calculateIP4'),
)

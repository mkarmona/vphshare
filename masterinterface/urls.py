from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render_to_response

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vphshare.views.home', name='home'),
    # url(r'^vphshare/', include('vphshare.foo.urls')),

    # admin/doc urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # admin urls
    url(r'^admin/', include(admin.site.urls)),

    # default roolback
    url(r'', include('social_auth.urls')),
    url(r'', include('masterinterface.scs.urls')),

    # add url for sendsmsworld
    url(r'^sendsmsworld/', include('masterinterface.sendsmsworld.urls'))
    ##NEW_URL
)

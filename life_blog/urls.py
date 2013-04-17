from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'life_blog.views.home', name='home'),
    # url(r'^life_blog/', include('life_blog.foo.urls')),

    url(r'^api-root/', include('api.urls', namespace='api')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

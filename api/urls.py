from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = format_suffix_patterns(patterns('api.views',
	url(r'^users/$', views.UserList.as_view()),
))

urlpatterns += patterns('',
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)

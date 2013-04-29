from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = format_suffix_patterns(patterns('api.views',
	url(r'^users/$', views.UserList.as_view()),
	url(r'^users/update_profile/$', views.UserUpdate.as_view()),
	url(r'^users/list_article/$', views.UserArticle.as_view()),
	url(r'^articles/$', views.ArticleList.as_view()),
	url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
))

urlpatterns += patterns('',
	url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
)

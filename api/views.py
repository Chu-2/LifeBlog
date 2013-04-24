from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsAuthor
from api.serializers import UserSerializer, ArticleSerializer
from articles.models import Article
from authors.models import Author

class ArticleList(generics.ListCreateAPIView):
	model = Article
	serializer_class = ArticleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def pre_save(self, obj):
		obj.author = self.request.user

	def get_queryset(self):
		return Article.objects.filter(public=True)

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Article
	serializer_class = ArticleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

	def pre_save(self, obj):
		obj.author = self.request.user

class UserList(generics.ListCreateAPIView):
	model = Author
	serializer_class = UserSerializer

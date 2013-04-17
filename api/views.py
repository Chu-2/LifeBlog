from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from articles.models import Article
from authors.models import Author
from api.permissions import IsAuthorOrReadOnly
from api.serializers import UserSerializer, ArticleSerializer

class ArticleList(generics.ListCreateAPIView):
	model = Article
	serializer_class = ArticleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

	def pre_save(self, obj):
		obj.author = self.request.user

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Article
	serializer_class = ArticleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

	def pre_save(self, obj):
		obj.author = self.request.user

class UserList(generics.ListCreateAPIView):
	model = Author
	serializer_class = UserSerializer

from django.db.models import F
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsAuthor
from api.serializers import (
	UserListSerializer,
	UserRegisterSerializer,
	UserUpdateSerializer,
	ArticleSerializer
)
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
		queryset = Article.objects.filter(public=True)
		order = self.request.QUERY_PARAMS.get('order', None)
		if order is not None:
			# really dislike this part of code, but I can't get Django's FieldError exception to work :/
			if (order == 'id' or order == '-id' or
				order == 'published' or order == '-published' or
				order == 'views' or order == '-views' or
				order == 'title' or order == '-title'):
				queryset = queryset.order_by(order)
		return queryset

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Article
	serializer_class = ArticleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

	def pre_save(self, obj):
		obj.author = self.request.user

	def get_queryset(self):
		queryset = Article.objects.filter(pk=self.kwargs['pk'])
		queryset.update(views=F('views')+1)
		return queryset

class UserList(generics.ListAPIView):
	model = Author
	serializer_class = UserListSerializer

	def get_queryset(self):
		queryset = Author.objects.all()
		order = self.request.QUERY_PARAMS.get('order', None)
		if order is not None:
			# really dislike this part of code, but I can't get Django's FieldError exception to work :/
			if order == 'age':
				queryset = queryset.order_by('-date_of_birth')
			elif order == '-age':
				queryset = queryset.order_by('date_of_birth')
			elif (order == 'id' or order == '-id' or
				  order == 'username' or order == '-username' or
				  order == 'first_name' or order == '-first_name' or
				  order == 'last_name' or order == '-last_name'):
				queryset = queryset.order_by(order)
		return queryset

class UserRegister(generics.CreateAPIView):
	model = Author
	serializer_class = UserRegisterSerializer

class UserUpdate(generics.UpdateAPIView):
	model = Author
	serializer_class = UserUpdateSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get_object(self):
		return self.request.user

class UserArticle(generics.ListAPIView):
	model = Article
	serializer_class = ArticleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	
	def get_queryset(self):
		return Article.objects.filter(author=self.request.user)

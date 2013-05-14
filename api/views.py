from django.db.models import F
from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsAuthor
from api.serializers import (
	UserListSerializer,
	UserRegisterSerializer,
	UserUpdateSerializer,
	ArticleListSerializer,
	ArticleCreateSerializer,
	ArticleDetailSerializer,
	CommentSerializer
)
from articles.models import Article
from authors.models import Author
from comments.models import Comment

ALLOWED_ARTICLE_ORDERS = ['id', '-id', 'published', '-published', 'views', '-views', 'title', '-title']
ALLOWED_USER_ORDERS = ['id', '-id', 'username', '-username', 'first_name', '-first_name', 'last_name', '-last_name', 'age', '-age']

class ArticleList(generics.ListAPIView):
	model = Article
	serializer_class = ArticleListSerializer

	def get_queryset(self):
		queryset = Article.objects.filter(public=True)
		order = self.request.QUERY_PARAMS.get('order', None)
		if order is not None and order in ALLOWED_ARTICLE_ORDERS:
			queryset = queryset.order_by(order)
		return queryset

class ArticleCreate(generics.CreateAPIView):
	model = Article
	serializer_class = ArticleCreateSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	
	def pre_save(self, obj):
		obj.author = self.request.user

class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
	model = Article
	serializer_class = ArticleDetailSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor)

	def pre_save(self, obj):
		obj.author = self.request.user

	def get_queryset(self):
		queryset = Article.objects.filter(pk=self.kwargs['pk'])
		queryset.update(views=F('views')+1)
		return queryset

class ArticleComment(generics.CreateAPIView):
	model = Comment
	serializer_class = CommentSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def pre_save(self, obj):
		obj.author = self.request.user
		obj.article = Article.objects.get(pk=self.kwargs['pk'])

class UserList(generics.ListCreateAPIView):
	model = Author
	serializer_class = UserListSerializer

	def get_queryset(self):
		queryset = Author.objects.all()
		order = self.request.QUERY_PARAMS.get('order', None)
		if order is not None and order in ALLOWED_USER_ORDERS:
			if order == 'age':
				queryset = queryset.order_by('-date_of_birth')
			elif order == '-age':
				queryset = queryset.order_by('date_of_birth')
			else:
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
	serializer_class = ArticleListSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)
	
	def get_queryset(self):
		return Article.objects.filter(author=self.request.user)

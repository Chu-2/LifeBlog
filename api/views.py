from django.db.models import F
from datetime import date, timedelta
from itertools import chain
from rest_framework import filters
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


class ArticleList(generics.ListAPIView):
    model = Article
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        """
        queryset = Article.objects.filter(public=True)
        order = self.request.QUERY_PARAMS.get('order', None)
        if order is not None and order in ALLOWED_ARTICLE_ORDERS:
            queryset = queryset.order_by(order)
        """

        queryset = Article.objects.filter(public=True)
        results = self.request.QUERY_PARAMS.get('results', None)
        if results is not None and results == 'all':
            return queryset

        today = date.today()

        start_date = today.replace(year=today.year-13) + timedelta(days=1)
        end_date = today
        q1 = queryset.filter(author__date_of_birth__range=(start_date, end_date))[:8]

        start_date = today.replace(year=today.year-19) + timedelta(days=1)
        end_date = today.replace(year=today.year-13)
        q2 = queryset.filter(author__date_of_birth__range=(start_date, end_date))[:8]

        start_date = today.replace(year=today.year-36) + timedelta(days=1)
        end_date = today.replace(year=today.year-19)
        q3 = queryset.filter(author__date_of_birth__range=(start_date, end_date))[:8]

        start_date = today.replace(year=today.year-61) + timedelta(days=1)
        end_date = today.replace(year=today.year-36)
        q4 = queryset.filter(author__date_of_birth__range=(start_date, end_date))[:8]

        q5 = queryset.filter(author__date_of_birth__lte=today.replace(year=today.year-61))[:8]

        return chain(q1, q2, q3, q4, q5)


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


class UserList(generics.ListAPIView):
    model = Author
    serializer_class = UserListSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id', 'username', 'first_name', 'last_name', 'date_of_birth')


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
    filter_backends = (filters.OrderingFilter,)
    ordering = ('id', 'published', 'views', 'title')

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

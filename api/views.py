from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from authors.models import Author
from api.serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
	model = Author
	serializer_class = UserSerializer

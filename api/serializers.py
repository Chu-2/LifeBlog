from django import forms
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from articles.models import Article
from authors.models import Author

HIDDEN_PASSWORD_STRING = '<hidden>'

class PasswordField(serializers.CharField):
	"""Special field to update a password field."""
	widget = forms.widgets.PasswordInput

	def from_native(self, value):
		"""Hash if new value sent, else retrieve current password"""
		if value == HIDDEN_PASSWORD_STRING or value == '':
			return self.parent.object.password
		else:
			return make_password(value)

	def to_native(self, value):
		"""Hide hashed-password in API display"""
		return HIDDEN_PASSWORD_STRING

class ArticleSerializer(serializers.ModelSerializer):
	author = serializers.Field(source='author.username')

	class Meta:
		model = Article
		fields = ('id', 'author', 'published', 'public', 'views', 'title', 'body')

class UserListSerializer(serializers.ModelSerializer):
	age = serializers.Field(source='get_age')
	# articles = serializers.PrimaryKeyRelatedField(many=True)

	class Meta:
		model = Author
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'age')

class UserRegisterSerializer(serializers.ModelSerializer):
	password = PasswordField()

	class Meta:
		model = Author
		fields = ('username', 'password', 'date_of_birth', 'email', 'first_name', 'last_name')
		
class UserUpdateSerializer(serializers.ModelSerializer):
	password = PasswordField()

	class Meta:
		model = Author
		fields = ('password', 'date_of_birth', 'email', 'first_name', 'last_name')

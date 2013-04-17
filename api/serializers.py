from django import forms
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
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

class UserSerializer(serializers.ModelSerializer):
	password = PasswordField()

	class Meta:
		model = Author
		fields = ('id', 'username', 'password', 'date_of_birth', 'email', 'first_name', 'last_name')

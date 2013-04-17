from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class Author(AbstractUser):
	date_of_birth = models.DateField()

	custom_objects = UserManager()

	REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['date_of_birth']

	class Meta:
		app_label = 'authors'

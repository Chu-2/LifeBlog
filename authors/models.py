from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from datetime import date


class Author(AbstractUser):
    date_of_birth = models.DateField()

    custom_objects = UserManager()

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['date_of_birth']

    def get_age(self):
        today = date.today()
        born = self.date_of_birth
        try:
            birthday = born.replace(year=today.year)
        except ValueError:  # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        return today.year - born.year - (birthday > today)

    class Meta:
        app_label = 'authors'
        ordering = ['date_joined']

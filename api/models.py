from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from authors.models import Author


# Ensures that each user is given an auth token with which to access the
# application's REST API. Called after a user is created.
@receiver(post_save, sender=Author)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

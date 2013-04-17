from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from authors.models import Author

@receiver(post_save, sender=Author)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

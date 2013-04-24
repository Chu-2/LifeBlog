from django.db import models

class Article(models.Model):
	published = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=False)
	title = models.CharField(max_length=100, blank=True, default='')
	body = models.TextField()
	author = models.ForeignKey('authors.Author', related_name='articles')

	class Meta:
		ordering = ('published',)
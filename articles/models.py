from django.db import models
from comments.models import Comment

class Article(models.Model):
	published = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=False)
	views = models.IntegerField(default=0)
	title = models.CharField(max_length=100, blank=True, default='')
	body = models.TextField()
	author = models.ForeignKey('authors.Author', related_name='articles')

	def count_comments(self):
		return Comment.objects.filter(article=self).count()
		
	class Meta:
		ordering = ('published',)
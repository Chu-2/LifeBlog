from django.db import models

class Article(models.Model):
	published = models.DateTimeField(auto_now_add=True)
	public = models.BooleanField(default=False)
	views = models.IntegerField(default=0)
	title = models.CharField(max_length=100, blank=True, default='')
	body = models.TextField()
	author = models.ForeignKey('authors.Author', related_name='articles')

	def count_comments(self):
		return self.comments.all().count()

	def get_age_range(self):
		age = self.author.get_age()
		if age <= 12:
			return 1
		elif age > 12 and age <= 18:
			return 2
		elif age > 18 and age <= 35:
			return 3
		elif age > 35 and age <= 60:
			return 4
		else:
			return 5
		return age

	class Meta:
		ordering = ('published',)
from django.db import models


class Comment(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField()
    author = models.ForeignKey('authors.Author', related_name='comments')
    article = models.ForeignKey('articles.Article', related_name='comments')

    class Meta:
        ordering = ('published',)

from django.db import models
import Image


class Article(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField()
    background = models.ImageField(upload_to='article_bg', blank=True, null=True)
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

    """
    def save(self, size=(200, 200)):
        super(Article, self).save()

        pw = self.background.width
        ph = self.background.height
        nw = size[0]
        nh = size[1]

        # only do this if the image needs resizing
        if (pw, ph) != (nw, nh):
            filename = str(self.background.path)
            image = Image.open(filename)
            pr = float(pw) / float(ph)
            nr = float(nw) / float(nh)

            if pr > nr:
                # photo aspect is wider than destination ratio
                tw = int(round(nh * pr))
                image = image.resize((tw, nh), Image.ANTIALIAS)
                l = int(round(( tw - nw ) / 2.0))
                image = image.crop((l, 0, l + nw, nh))
            elif pr < nr:
                # photo aspect is taller than destination ratio
                th = int(round(nw / pr))
                image = image.resize((nw, th), Image.ANTIALIAS)
                t = int(round(( th - nh ) / 2.0))
                print((0, t, nw, t + nh))
                image = image.crop((0, t, nw, t + nh))
            else:
                # photo aspect matches the destination ratio
                image = image.resize(size, Image.ANTIALIAS)

            image.save(filename)

    def __unicode__(self):
        return self.title
    """

    class Meta:
        ordering = ('published',)

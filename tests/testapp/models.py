from django.db import models

class BlogPost(models.Model):

    title = models.CharField(max_length=255)
    body = models.TextField()
    pub_date = models.DateField()
    slug = models.SlugField(max_length=255)

    def get_absolute_url(self):
        return '%s/%s/%s/%s' % (self.pub_date.year, self.pub_date.strftime('%m'), self.pub_date.strftime('%d'))
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_text
from django.utils.text import slugify


def upload_loc(instance, filename):
    return "%s/%s" % (instance, filename)


class Album(models.Model):
    title = models.CharField(max_length=30, verbose_name='Album_title')
    artist = models.CharField(max_length=20)
    slug = models.SlugField(null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    create_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.FileField(upload_to=upload_loc)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(self.title + "_ _" + self.artist)

    def get_absolute_url(self):
        return reverse('music:Album_detail', kwargs={'album_id': self.id})


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    artist = models.CharField(max_length=20, default='unknown')
    song_label = models.CharField(max_length=10)
    song = models.FileField(upload_to=upload_loc)

    def __str__(self):
        return smart_text(self.title)






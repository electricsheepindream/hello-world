from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from music.models import Album
# Create your models here.


class Comments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-time']

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comments.objects.filter(parent=self)

    @property
    def is_parents(self):
        if self.parent is not None:
            return False
        else:
            return True



from django.contrib import admin
from .models import Album, Song


class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "update_date", "create_date"]
    readonly_fields = ['update_date', 'create_date']

    class Meta:
        module = Album


class SongAdmin(admin.ModelAdmin):
    list_display = ["album", "title"]

    class Meta:
        module = Song

admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)

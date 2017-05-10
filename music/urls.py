from django.conf.urls import url
from . import views


app_name = "music"
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^(?P<album_id>\d+)/$', views.detail, name='Album_detail'),

    url(r'^album_create/$', views.album_create, name='album_create'),

    url(r'^album_update/(?P<album_id>\d+)/$', views.album_update, name='album_update'),

    url(r'^album_delete/(?P<album_id>\d+)/$', views.album_delete, name='album_delete'),

    url(r'^(?P<album_id>\d+)/song_create/$', views.song_create, name='song_create'),

    url(r'^(?P<song_id>\d+)/song_update/$', views.song_update, name='song_update'),

    url(r'^song_delete/(?P<song_id>\d+)/$', views.song_delete, name='song_delete'),

    url(r'^user_create/$', views.user_create, name='user_create'),

    url(r'^user_login/$', views.user_login, name='user_login'),

    url(r'^user_logout/$', views.user_logout, name='user_logout'),
]
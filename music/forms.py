from django import forms
from .models import Album, Song
from django.contrib.auth.models import User


class AlbumForms(forms.ModelForm):
    class Meta:
        model = Album
        fields = ["title", "artist", "image"]


class SongForms(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title", "song_label", "song"]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
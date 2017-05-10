from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import AlbumForms, SongForms, UserForm, LoginForm
from .models import Album, Song
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def index(request):
    queryset_list = Album.objects.all()
    hello = "Hello %s" % (request.user)
    query = request.GET.get('w')
    if query:
        queryset_list = queryset_list.filter(
            Q(title__contains=query) |
            Q(artist__contains=query)
        ).order_by('update_date')
    paginator = Paginator(queryset_list, 9)  # Show 2 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    page_num = queryset.paginator.num_pages
    page_set = []
    for i in range(1, page_num+1):
        page_set.append(i)
    context = {
        "query": queryset,
        'greet': hello,
        'page_set': page_set
    }
    return render(request, 'index.html', context)


def album_create(request):
    form = AlbumForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'album_form.html', context)


@login_required(login_url='/music/user_login/')
def album_update(request, album_id=None):
    instance = get_object_or_404(Album, id=album_id)
    form = AlbumForms(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
        'title': instance.title,
        'instance': instance,
    }
    return render(request, 'album_form.html', context)


@login_required(login_url='/music/user_login/')
def album_delete(request, album_id=None):
    instance = get_object_or_404(Album, id=album_id)
    instance.delete()
    return redirect("music:index")


def detail(request, album_id):
    instance = get_object_or_404(Album, id=album_id)
    song = instance.song_set.all()
    context = {
        "song": song,
        "instance": instance
    }
    return render(request, 'detail.html', context)


def song_create(request, album_id=None):
    instance = get_object_or_404(Album, id=album_id)
    form = SongForms(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.album = instance
        obj.artist = instance.artist
        obj.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'album_form.html', context)


@login_required(login_url='/music/user_login/')
def song_update(request, song_id=None):
    instance = get_object_or_404(Song, id=song_id)
    album = instance.album
    form = SongForms(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(album.get_absolute_url())
    context = {
        'form': form,
        'title': instance.title,
        'instance': instance,
    }
    return render(request, 'album_form.html', context)


@login_required(login_url='/music/user_login/')
def song_delete(request, song_id=None):
    instance = get_object_or_404(Song, id=song_id)
    instance.delete()
    return redirect("music:index")


def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect("music:index")
    context = {
        'form': form,
    }
    return render(request, 'album_form.html', context)


def user_login(request):
    if request.user.is_authenticated():
        return redirect("music:index")
    else:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("music:index")
        context = {
                'form': form,
            }
        return render(request, 'album_form.html', context)


def user_logout(request):
    logout(request)
    return redirect("music:index")
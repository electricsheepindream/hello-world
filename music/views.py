from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import AlbumForms, SongForms, UserForm, LoginForm
from .models import Album, Song
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.models import Comments
from comments.forms import CommentsForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


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
    initial_data = {
        'content_type': ContentType.objects.get_for_model(Album),
        'object_id': instance.id
    }
    comment_form = CommentsForm(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        parent_obj = None
        try:
            parent_id = int(request.POST.get('com_id'))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comments.objects.filter(id=parent_id)

            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
        object_id = comment_form.cleaned_data.get('object_id')
        content = comment_form.cleaned_data.get('content')
        Comments.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content,
            parent=parent_obj,
        )
        return HttpResponseRedirect(instance.get_absolute_url())

    content_type = ContentType.objects.get_for_model(Album)
    obj_id = instance.id
    comments = Comments.objects.filter(content_type=content_type, object_id=obj_id)
    main_comments = comments.filter(parent=None)
    context = {
        "song": song,
        "instance": instance,
        "comments": comments,
        "comment_form": comment_form,
        "main_comments": main_comments,
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
        send_mail(
            'Subject here',
            'Here is the message.',
            'electricsheepindream@gmail.com',
            [email],
            fail_silently=False,
        )
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
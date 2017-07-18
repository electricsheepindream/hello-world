import django
from django.shortcuts import render
from django.conf import settings
# Create your views here.
from django.core.mail import send_mail

send_mail(
    'Subject here',
    'Here is the message.',
    'electricsheepindream@gmail.com',
    ['electricsheep@email.com'],
    fail_silently=False,
)
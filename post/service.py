from django.shortcuts import render, redirect
from storages.backends.s3boto3 import S3Boto3Storage

from .forms import *


def user_registr(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


class MediaStorage(S3Boto3Storage):
    """Менеджер медиа файлов AWS S3"""
    location = 'media'
    file_overwrite = False